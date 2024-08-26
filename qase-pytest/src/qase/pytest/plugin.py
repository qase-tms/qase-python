import pathlib
from typing import Tuple, Union
import mimetypes

from qase.commons.models.result import Result, Field
from qase.commons.models.attachment import Attachment
from qase.commons.models.suite import Suite
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
        self.run_id = None
        self.execution_plan = reporter.get_execution_plan()

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
                    param_name, values = mark.args
                    if ',' in param_name:
                        grouped_params.append(param_name.split(','))

            # Attach the captured params to the test item
            item._grouped_params = grouped_params

        # Filter test cases based on ids
        if self.execution_plan:
            items[:] = [item for item in items if
                        item.get_closest_marker('qase_id') and item.get_closest_marker('qase_id').kwargs.get(
                            "id") in self.execution_plan]

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

        self.reporter.complete_run()

    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_protocol(self, item):
        self.ignore = True if item.get_closest_marker("qase_ignore") else False

        if not self.ignore:
            self.reporter.enable_profilers()
            self.start_pytest_item(item)
            yield
            self.finish_pytest_item(item)
            self.reporter.disable_profilers()
        else:
            yield

    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_makereport(self, item, call):
        if not self.ignore:
            report = (yield).get_result()

            def set_result(res):
                self.runtime.result.execution.status = res

            def _attach_logs():
                # TODO: can be attached twice
                if report.caplog:
                    self.add_attachments((report.caplog, "text/plain", "log.txt"))
                if report.capstdout:
                    self.add_attachments((report.capstdout, "text/plain", "stdout.txt"))
                if report.capstderr:
                    self.add_attachments((report.capstderr, "text/plain", "stderr.txt"))

            if report.longrepr:
                self.runtime.result.execution.stacktrace = report.longreprtext

            if report.failed:
                if call.excinfo.typename != "AssertionError":
                    set_result(PYTEST_TO_QASE_STATUS['BROKEN'])
                else:
                    set_result(PYTEST_TO_QASE_STATUS['FAILED'])
                self.runtime.result.add_message(call.excinfo.exconly())
            elif report.skipped:
                if self.runtime.result.execution.status in (
                        None,
                        PYTEST_TO_QASE_STATUS['PASSED'],
                ):
                    set_result(PYTEST_TO_QASE_STATUS['SKIPPED'])
            else:
                if self.runtime.result.execution.status is None:
                    set_result(PYTEST_TO_QASE_STATUS['PASSED'])

            if self.reporter.config.framework.pytest.capture_logs and report.when == "call":
                _attach_logs()
        else:
            yield

    def start_pytest_item(self, item):
        self.runtime.result = Result(
            title=self._get_title(item),
            signature='',
        )
        self._set_fields(item)
        self._set_tags(item)
        self._set_author(item)
        self._set_muted(item)
        self._set_testops_id(item)
        self._set_params(item)
        self._set_suite(item)
        self._set_relations(item)
        self._get_signature(item)

    def finish_pytest_item(self, item):
        self.runtime.result.execution.complete()
        self.runtime.result.add_steps([step for key, step in self.runtime.steps.items()])
        self.reporter.add_result(self.runtime.result)

        self.runtime = Runtime()

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

            attachment = Attachment(file_name=filename, content=content, mime_type=mime, file_path=file_path)
            self.runtime.add_attachment(attachment)

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
        self.runtime.result.signature = item.nodeid.replace("/", "::")
        if self.runtime.result.testops_id:
            self.runtime.result.signature += f"::{self.runtime.result.testops_id}"
        for key, val in self.runtime.result.params.items():
            self.runtime.result.signature += f"::{{{key}:{val}}}"

    def _set_relations(self, item) -> None:
        # TODO: Add support for relations
        pass

    def _set_fields(self, item) -> None:
        # Legacy fields support
        for name in ["description", "preconditions", "postconditions", "layer", "severity", "priority"]:
            try:
                self.runtime.result.add_field(Field(name, item.get_closest_marker("qase_" + name).kwargs.get(name)))
            except:
                pass

        try:
            fields = item.get_closest_marker("qase_fields").kwargs.get("fields")
            for name, field in fields:
                self.runtime.result.add_field(Field(name, field))
        except:
            pass

    def _set_tags(self, item) -> None:
        try:
            tags = item.get_closest_marker("qase_tags").kwargs.get("tags")
            for tag in tags:
                self.runtime.result.add_tag(tag)
        except:
            pass

    def _set_author(self, item) -> None:
        try:
            self.runtime.result.author = str(item.get_closest_marker("qase_author").kwargs.get("author"))
        except:
            pass

    def _set_muted(self, item) -> None:
        try:
            self.runtime.result.muted = True if item.get_closest_marker("qase_muted").kwargs.get("muted") else False
        except:
            pass

    def _set_testops_id(self, item) -> None:
        try:
            self.runtime.result.testops_id = int(item.get_closest_marker("qase_id").kwargs.get("id"))
        except:
            pass

    def _set_params(self, item) -> None:
        if hasattr(item, 'callspec'):
            for group in item._grouped_params:
                self.runtime.result.add_param_groups(group)

            for key, val in item.callspec.params.items():
                if key.startswith("__pytest"):
                    continue
                self.runtime.result.add_param(key, str(val))

    def _set_suite(self, item) -> None:
        marker = item.get_closest_marker("qase_suite")
        if marker:
            self.runtime.result.suite = Suite(marker.kwargs.get("title"), marker.kwargs.get("description"))
            return
        self._get_suite(item)

    def _get_suite(self, item):
        path, class_name, tail = islice(chain(item.nodeid.split('::'), [None], [None]), 3)

        class_name = class_name if tail else None
        file_name, file_path = islice(chain(reversed(path.rsplit('/', 1)), [None]), 2)

        module = file_name.split('.')[0]
        package = path.replace('/', '.') if path else None

        if file_path:
            title = file_path + '.' + module
        else:
            title = module

        if class_name:
            title += '.' + class_name

        self.runtime.result.suite = Suite(title, package)


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
