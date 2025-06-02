import os
import pathlib
import re
from typing import Tuple, Union, List
import mimetypes

from qase.commons.models import Relation
from qase.commons.models.config.framework import Trace, Video
from qase.commons.models.relation import SuiteData
from qase.commons.models.result import Result, Field
from qase.commons.models.attachment import Attachment
from qase.commons.models.runtime import Runtime

from qase.commons import QaseUtils

from filelock import FileLock
from itertools import chain, islice

PYTEST_TO_QASE_STATUS = {
    "PASSED": 'passed',
    "FAILED": 'failed',
    "SKIPPED": 'skipped',
    "BLOCKED": 'blocked',
    "BROKEN": 'invalid'
}

try:
    from xdist import is_xdist_controller
except ImportError:
    def is_xdist_controller(*args, **kwargs):
        return True

try:
    import pytest
except ImportError:
    raise ImportError("pytest is not installed")


class PluginNotInitializedException(Exception):
    pass


class QasePytestPlugin:
    run = None
    meta_run_file = pathlib.Path("src.run")

    def __init__(
            self,
            reporter
    ):
        self.runtime = Runtime()
        self.reporter = reporter
        self.config = reporter.config
        self.run_id = None
        self.execution_plan = reporter.get_execution_plan()
        self._current_item = None
        self.ignore = None

        self.reporter.setup_profilers(runtime=self.runtime)

    def start_step(self, step):
        self.runtime.add_step(step)

    def finish_step(self, id, exception=None):
        status = PYTEST_TO_QASE_STATUS['PASSED']
        if exception:
            status = PYTEST_TO_QASE_STATUS['FAILED']

        self.runtime.finish_step(id, status=status)

    @staticmethod
    def drop_run_id():
        if QasePytestPlugin.meta_run_file.exists():
            QasePytestPlugin.meta_run_file.unlink()

    def pytest_collection_modifyitems(self, session, config, items):
        """
        Modify collected test items to inject our parameter capturing logic.
        """
        for item in items:
            grouped_params = []

            # Extract single and grouped params from the item's markers
            for mark in item.iter_markers():
                if mark.name == 'parametrize':
                    if len(mark.args) != 0:
                        param_name, values = mark.args
                        if ',' in param_name:
                            grouped_params.append(
                                [item.strip() for item in param_name.split(',')])
                    else:
                        param_name = mark.kwargs.get('argnames')
                        if ',' in param_name:
                            grouped_params.append(
                                [item.strip() for item in param_name.split(',')])

            # Attach the captured params to the test item
            item._grouped_params = grouped_params

        # Filter test cases based on ids
        if self.execution_plan:
            new_items = []
            for item in items:
                if item.get_closest_marker('qase_id'):
                    ids = QasePytestPlugin._get_qase_ids(item)
                    if any(id in self.execution_plan for id in ids):
                        new_items.append(item)

            items[:] = new_items

    def pytest_sessionstart(self, session):
        if is_xdist_controller(session):
            self.run_id = self.reporter.start_run()
            with FileLock("qase.lock"):
                if self.run_id:
                    with open(self.meta_run_file, "w") as lock_file:
                        lock_file.write(str(self.run_id))
        else:
            self.load_run_from_lock()

    def pytest_sessionfinish(self, session, exitstatus):
        if is_xdist_controller(session):
            QasePytestPlugin.drop_run_id()
        else:
            self.reporter.complete_worker()

        if not QasePytestPlugin.meta_run_file.exists():
            self.reporter.complete_run()

    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_protocol(self, item):
        self.ignore = True if item.get_closest_marker("qase_ignore") else False

        if not self.ignore:
            self.reporter.enable_profilers()
            self.start_pytest_item(item)
            self._current_item = item
            yield
            self._current_item = None
            self.reporter.disable_profilers()
        else:
            yield

    @pytest.hookimpl
    def pytest_runtest_logfinish(self):
        if not self.ignore and self._current_item:
            self.finish_pytest_item()
            self.start_pytest_item(self._current_item)

    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_makereport(self, item, call):
        if self.ignore:
            yield
            return

        report = (yield).get_result()

        # Skip processing if not in the relevant phase
        if call.when not in ["setup", "call"]:
            return

        # Process test result and update status
        self._process_test_result(report, call, item)

        # Add logs if configured and in call phase
        if self.reporter.config.framework.pytest.capture_logs and call.when == "call":
            self._attach_logs(report)

        # Handle xfail message in call phase
        if (call.when == "call" and
                self.__is_xfail_mark(report) and
                self.runtime.result.execution.status != PYTEST_TO_QASE_STATUS['PASSED']):
            self.runtime.result.add_message(report.wasxfail)

        # Handle skip message in setup phase
        if (call.when == "setup" and
                report.longrepr and
                self.runtime.result.execution.status == PYTEST_TO_QASE_STATUS['SKIPPED']):
            self.runtime.result.add_message(report.longrepr[2].split(":")[1])

        # Handle Playwright artifacts if applicable
        if call.when == "call":
            self._process_playwright_artifacts(item)

    def _process_test_result(self, report, call, item):
        """Process test results and set appropriate status."""
        # Add stacktrace if available
        if report.longrepr:
            self.runtime.result.execution.stacktrace = report.longreprtext

        # Handle failed tests
        if report.failed:
            self._handle_failed_test(call)
        # Handle skipped tests
        elif report.skipped:
            self._handle_skipped_test(report, call)
        # Handle passed tests
        else:
            self._handle_passed_test(report, call)

    def _handle_failed_test(self, call):
        """Handle failed test case and set appropriate status."""
        is_assertion_error = call.excinfo.typename == "AssertionError"
        status = PYTEST_TO_QASE_STATUS['FAILED'] if is_assertion_error else PYTEST_TO_QASE_STATUS['BROKEN']
        self._set_result_status(status)
        self.runtime.result.add_message(call.excinfo.exconly())

    def _handle_skipped_test(self, report, call):
        """Handle skipped test case and set appropriate status."""
        xfail_status = self._get_xfail_status(report, call)
        if xfail_status:
            self._set_result_status(xfail_status)
        elif self.runtime.result.execution.status in (None, PYTEST_TO_QASE_STATUS['PASSED']):
            self._set_result_status(PYTEST_TO_QASE_STATUS['SKIPPED'])

    def _handle_passed_test(self, report, call):
        """Handle passed test case and set appropriate status."""
        xfail_status = self._get_xfail_status(report, call)
        if xfail_status:
            self._set_result_status(xfail_status)
        elif self.runtime.result.execution.status is None:
            self._set_result_status(PYTEST_TO_QASE_STATUS['PASSED'])

    def _get_xfail_status(self, report, call):
        """Get xfail status if applicable."""
        if self.__is_xfail_mark(report) and call.when == "call":
            status = self.config.framework.pytest.xfail_status
            return status.xfail if report.skipped else status.xpass
        return None

    def _set_result_status(self, status):
        """Set test result execution status."""
        self.runtime.result.execution.status = status

    def _attach_logs(self, report):
        """Attach logs to the test result."""
        logs = [
            (report.caplog, "text/plain", "log.txt"),
            (report.capstdout, "text/plain", "stdout.txt"),
            (report.capstderr, "text/plain", "stderr.txt"),
        ]
        for content, mime_type, filename in logs:
            if content:
                self.add_attachments((content, mime_type, filename))

    def _process_playwright_artifacts(self, item):
        """Process and attach Playwright artifacts if available."""
        if not (hasattr(item, 'funcargs') and 'page' in item.funcargs):
            return

        page = item.funcargs['page']
        if not hasattr(page, 'video'):
            return

        folder_name = self.__build_folder_name(item)
        output_dir = self.config.framework.playwright.output_dir
        base_path = os.path.join(os.getcwd(), output_dir, folder_name)

        # Attach video if enabled
        if self.config.framework.playwright.video != Video.off:
            video_path = os.path.join(base_path, "video.webm")
            self.add_attachments(video_path)

        # Attach trace if enabled
        if self.config.framework.playwright.trace != Trace.off:
            trace_path = os.path.join(base_path, "trace.zip")
            self.add_attachments(trace_path)

    def start_pytest_item(self, item):
        self.runtime.result = Result(
            title=self._get_title(item),
            signature='',
        )
        self._set_fields(item)
        self._set_author(item)
        self._set_muted(item)
        self._set_testops_ids(item)
        self._set_params(item)
        self._set_suite(item)
        self._set_relations(item)
        self._get_signature(item)

    def finish_pytest_item(self):
        self.runtime.result.execution.complete()
        self.runtime.result.add_steps(
            [step for key, step in self.runtime.steps.items()])
        self.reporter.add_result(self.runtime.result)

        self.runtime.clear()

    def add_attachments(
            self, *files: Union[str, Tuple[str, str], Tuple[bytes, str, str]]
    ):
        for file in files:
            filename = None
            content = None
            file_path = None

            if isinstance(file, tuple):
                if len(file) == 2:
                    file_path, mime = file
                    filename = QaseUtils.get_filename(file_path)
                else:
                    content, mime, filename = file
            elif isinstance(file, str):
                file_path = file
                mime = mimetypes.guess_type(file)[0]
                filename = QaseUtils.get_filename(file_path)

            attachment = Attachment(
                file_name=filename, content=content, mime_type=mime, file_path=file_path)
            self.runtime.add_attachment(attachment)

    def add_param(self, name: str, value: str):
        """
        Add a parameter to the current test result.
        """
        if not self.runtime.result:
            return
        self.runtime.result.add_param(name, value)

    def load_run_from_lock(self):
        if QasePytestPlugin.meta_run_file.exists():
            with open(QasePytestPlugin.meta_run_file, "r") as lock_file:
                try:
                    self.run_id = str(lock_file.read())
                    self.reporter.set_run_id(self.run_id)
                except ValueError:
                    pass
        else:
            self.run_id = self.reporter.start_run()

    def _get_title(self, item):
        title = None
        try:
            title = item.get_closest_marker("qase_title").kwargs.get("title")
        except:
            pass

        if not title:
            title = item.originalname

        return str(title)

    def _get_signature(self, item):
        self.runtime.result.signature = QaseUtils.get_signature(
            self.runtime.result.testops_ids, item.nodeid.split("/"), self.runtime.result.params)

    def _set_relations(self, item) -> None:
        # TODO: Add support for relations
        pass

    def _set_fields(self, item) -> None:
        # Legacy fields support
        for name in ["description", "preconditions", "postconditions", "layer", "severity", "priority", "suite"]:
            try:
                self.runtime.result.add_field(
                    Field(name, item.get_closest_marker("qase_" + name).kwargs.get(name)))
            except:
                pass

        try:
            fields = item.get_closest_marker(
                "qase_fields").kwargs.get("fields")
            for name, field in fields:
                self.runtime.result.add_field(Field(name, field))
        except:
            pass

    def _set_author(self, item) -> None:
        try:
            author = str(item.get_closest_marker(
                "qase_author").kwargs.get("author"))
            if author != "None":
                self.runtime.result.add_field(Field("author", author))
        except:
            pass

    def _set_muted(self, item) -> None:
        try:
            muted = True if item.get_closest_marker("qase_muted") else False
            if muted:
                self.runtime.result.add_field(Field("muted", "true"))
        except:
            pass

    def _set_testops_ids(self, item) -> None:
        try:
            self.runtime.result.testops_ids = QasePytestPlugin._get_qase_ids(
                item)
        except:
            pass

    def _set_params(self, item) -> None:
        if hasattr(item, 'callspec'):
            # Get parameters that should be ignored
            ignored_params = set()
            for mark in item.iter_markers():
                if mark.name == 'qase_parametrize_ignore':
                    param_name = mark.kwargs.get('argnames')
                    if param_name:
                        if ',' in param_name:
                            ignored_params.update(
                                [p.strip() for p in param_name.split(',')])
                        else:
                            ignored_params.add(param_name)

            # Add grouped parameters that are not ignored
            for group in item._grouped_params:
                if not any(param in ignored_params for param in group):
                    self.runtime.result.add_param_groups(group)

            # Add individual parameters that are not ignored
            ids = item.callspec.id.split("-")
            if len(ids) != len(item.callspec.params.items()):
                for key, val in item.callspec.params.items():
                    if key.startswith("__pytest") or key in ignored_params:
                        continue
                    self.runtime.result.add_param(key, str(val))
            else:
                i = 0
                for key, val in item.callspec.params.items():
                    if key.startswith("__pytest") or key in ignored_params:
                        i += 1
                        continue
                    value = str(ids[i])
                    i += 1
                    self.runtime.result.add_param(key, value)

    def _set_suite(self, item) -> None:
        marker = item.get_closest_marker("qase_suite")
        if marker:
            self.runtime.result.relations = self.__prepare_relations(
                marker.kwargs.get("title").split('.'))
            return
        self._get_suite(item)

    def _get_suite(self, item):
        path, class_name, tail = islice(
            chain(item.nodeid.split('::'), [None], [None]), 3)

        class_name = class_name if tail else None
        file_name, file_path = islice(
            chain(reversed(path.rsplit('/', 1)), [None]), 2)

        module = file_name.split('.')[0]

        if file_path:
            title = file_path + '.' + module
        else:
            title = module

        if class_name:
            title += '.' + class_name

        self.runtime.result.relations = self.__prepare_relations(
            title.split('.'))

    @staticmethod
    def __prepare_relations(suites: []):
        relation = Relation()

        for suite in suites:
            relation.add_suite(SuiteData(title=suite))

        return relation

    @staticmethod
    def __build_folder_name(item):
        path_parts = [
            QasePytestPlugin.__sanitize_path_component(item.location[0])]

        if '.' in item.location[2]:
            path_parts.append(
                QasePytestPlugin.__sanitize_path_component(
                    item.location[2].split('.')[0])
            )

        path_parts.append(
            QasePytestPlugin.__sanitize_path_component(item.originalname)
        )

        if 'browser_name' in item.funcargs:
            path_parts.append(item.funcargs['browser_name'])

        return "-".join(path_parts)

    @staticmethod
    def __sanitize_path_component(component):
        return component.replace(os.sep, "-").replace(".", "-").replace("_", "-").lower()

    @staticmethod
    def __is_xfail_mark(report):
        """Check if the test is marked as xfail."""
        return hasattr(report, 'wasxfail')

    @staticmethod
    def _get_qase_ids(item) -> Union[None, List[int]]:
        ids = item.get_closest_marker("qase_id").kwargs.get("id")
        if ids is None:
            return None
        if isinstance(ids, int):
            return [ids]
        else:
            return [int(i) for i in re.split(r'\s*,\s*', ids)]


class QasePytestPluginSingleton:
    _instance = None

    @staticmethod
    def init(**kwargs):
        if QasePytestPluginSingleton._instance is None:
            QasePytestPluginSingleton._instance = QasePytestPlugin(**kwargs)

    @staticmethod
    def get_instance() -> QasePytestPlugin:
        """ Static access method"""
        if QasePytestPluginSingleton._instance is None:
            raise PluginNotInitializedException("Init plugin first")
        return QasePytestPluginSingleton._instance

    def __init__(self):
        """ Virtually private constructor"""
        raise Exception("Use get_instance()")
