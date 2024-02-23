import pathlib
from typing import Tuple, Union
import pytest
import mimetypes
import re

from qaseio.commons.models.result import Result, Field
from qaseio.commons.models.attachment import Attachment
from qaseio.commons.models.suite import Suite
from qaseio.commons.utils import QaseUtils
from qaseio.commons.models.runtime import Runtime

from filelock import FileLock

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
            reporter,
            fallback,
            xdist_enabled = False,
            capture_logs = False,
            execution_plan = None,
            intercept_requests = False,
    ):
        self.runtime = Runtime()
        self.reporter = reporter
        self.run_id = None
        self.xdist_enabled = xdist_enabled
        self.fallback = fallback
        self.capture_logs = capture_logs
        self.debug = True
        self.execution_plan = execution_plan
        self.intercept_requests = intercept_requests
        self.interceptor = None
        if self.intercept_requests:
            # Lazy import
            from qaseio.commons.interceptor import InterceptorSingleton
            InterceptorSingleton.init(runtime=self.runtime)
            self.interceptor = InterceptorSingleton.get_instance()

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
        # Filter test cases based on ids
        if (self.execution_plan):
            items[:] = [item for item in items if item.get_closest_marker('qase_id') and item.get_closest_marker('qase_id').kwargs.get("id") in self.execution_plan]

    def pytest_sessionstart(self, session):
        if (not self.xdist_enabled) or (self.xdist_enabled and is_xdist_controller(session)):
            self.run_id = self.reporter.start_run()
            with FileLock("qaseio.lock"):
                if self.run_id:
                    with open(self.meta_run_file, "w") as lock_file:
                        lock_file.write(str(self.run_id))
        else:
            self.load_run_from_lock()
        self.has_started = True

    def pytest_sessionfinish(self, session, exitstatus):
        main = False
        if (not self.xdist_enabled) or (self.xdist_enabled and is_xdist_controller(session)):
            main = True
            QasePytestPlugin.drop_run_id()
        self.reporter.complete_run(main)
        self.has_started = False

    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_protocol(self, item):
        self.ignore = True if item.get_closest_marker("qase_ignore") else False

        if not self.ignore:
            # Capture HTTP requests inside test
            if self.interceptor:
                self.interceptor.enable()
            self.start_pytest_item(item)
            yield
            if self.interceptor:
                self.interceptor.disable()
            self.finish_pytest_item(item)
        else:
            yield

    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_makereport(self, item, call):
        if not self.ignore:
            report = (yield).get_result()
            def set_result(res):
                self.runtime.result.execution.status = res

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

            if self.capture_logs and report.when == "call":
                if report.caplog:
                    self.add_attachments((report.caplog, "text/plain", "log.txt"))
                if report.capstdout:
                    self.add_attachments((report.capstdout, "text/plain", "stdout.txt"))
                if report.capstderr:
                    self.add_attachments((report.capstderr, "text/plain", "stderr.txt"))
        else:
            yield

    def start_pytest_item(self, item):
        self.runtime.result = Result(
            title = self._get_title(item), 
            signature = self._get_signature(item),
            )
        self._set_fields(item)
        self._set_tags(item)
        self._set_author(item)
        self._set_muted(item)
        self._set_testops_id(item)
        self._set_params(item)
        self._set_suite(item)

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
    
    def _get_title(self, item):
        title = None
        try:
            title = item.get_closest_marker("qase_title").kwargs.get("title")
        except:
            pass

        if not title:
            title = item.originalname

        return str(title)
    
    def _get_signature(self, item) -> str:
        return re.sub(r'\[.*?\]', '', item.nodeid)
    
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
            for key, val in item.callspec.params.items():
                self.runtime.result.add_param(key, str(val))

    def _set_suite(self, item) -> None:
        marker = item.get_closest_marker("qase_suite")
        if marker:
            self.runtime.result.suite = Suite(marker.kwargs.get("title"), marker.kwargs.get("description"))


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
