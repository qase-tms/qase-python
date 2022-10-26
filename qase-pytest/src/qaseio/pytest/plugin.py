import pathlib
import time
from typing import Tuple, Union
import platform
import sys
import pip
import pytest
import uuid

from filelock import FileLock

QASE_MARKER = "qase"

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

class PluginNotInitializedException(Exception):
    pass

def get_platform():
    platform_data = {
        'os': platform.system(),
        'arch': platform.machine(),
        'python': '.'.join(map(str, sys.version_info)),
        'pip': pip.__version__
    }
    return ';'.join([f'{key}={value}' for key, value in platform_data.items()])

class QasePytestPlugin:
    run = None
    meta_run_file = pathlib.Path("src.run")

    def __init__(
            self,
            reporter
    ):
        self.reporter = reporter
        self.result = {}
        self.step_position = 1
        self.steps = {}
        self.step_uuid = None
        self.run_id = None

    def start_step(self, uuid):
        now = time.time()
        self.steps[uuid] = {
            "uuid": uuid,
            "started_at": now,
            "attachments": []
        }
        if self.step_uuid:
            self.steps[uuid]["parent_step_uuid"] = self.step_uuid

        self.step_uuid = uuid

    def finish_step(self, uuid, title, exception=None):
        status = PYTEST_TO_QASE_STATUS['PASSED']
        if exception:
            status = PYTEST_TO_QASE_STATUS['FAILED']
        
        self.steps[uuid]['status'] = status
        self.steps[uuid]['action'] = title
        self.steps[uuid]['position'] = self.step_position
        completed_at = time.time()
        self.steps[uuid]['duration'] = int((completed_at - self.steps[uuid].get("started_at")) * 1000)
        
        self.step_position = self.step_position+1
        self.step_uuid = self.steps[uuid].get("parent_step_uuid", None)

    @staticmethod
    def drop_run_id():
        if QasePytestPlugin.meta_run_file.exists():
            QasePytestPlugin.meta_run_file.unlink()

    def pytest_sessionstart(self, session):
        if is_xdist_controller(session):
            self.run_id = self.reporter.start_run()
            with FileLock("qaseio.lock"):
                if self.run_id:
                    with open(self.meta_run_file, "w") as lock_file:
                        lock_file.write(str(self.run_id))
        else:
            self.load_run_from_lock()

    def pytest_sessionfinish(self, session, exitstatus):
        self.reporter.finish()
        if is_xdist_controller(session):
            self.reporter.complete_run()
            QasePytestPlugin.drop_run_id()

    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_protocol(self, item):
        self.start_pytest_item(item)
        yield
        self.finish_pytest_item(item)

    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_makereport(self, item, call):
        report = (yield).get_result()
        def result(res):
            self.result["status"] = res

        if report.longrepr:
            self.result["stacktrace"] = report.longreprtext

        # Defining test result
        if report.when == "setup":
            result(None)

        if report.failed:
            if call.excinfo.typename != "AssertionError":
                result(PYTEST_TO_QASE_STATUS['BROKEN'])
            else:
                result(PYTEST_TO_QASE_STATUS['FAILED'])
            self.result["comment"] = call.excinfo.exconly()
        elif report.skipped:
            if self.result["status"] in (
                    None,
                    PYTEST_TO_QASE_STATUS['PASSED'],
            ):
                result(PYTEST_TO_QASE_STATUS['SKIPPED'])
        else:
            if self.result["status"] is None:
                result(PYTEST_TO_QASE_STATUS['PASSED'])
    
    def start_pytest_item(self, item):
        self.result = {
            'is_api_result': True,
            'case': {},
            'steps': {},
        }
        self.result['uuid'] = str(uuid.uuid4())
        self.result["started_at"] = time.time()

        try:
            case_id = item.get_closest_marker("qase_id").kwargs.get("id")
            self.result["case_id"] = int(case_id)
        except:
            pass
        
        title = ''
        try:
            title = item.get_closest_marker("qase_title").kwargs.get("title")
            self.result["case_id"] = int(case_id)
        except:
            pass

        if not title:
            title = item.originalname
        
        self.result["case"]["title"] = str(title)
        
        try:
            self.result["case"]["description"] = item.get_closest_marker("qase_description").kwargs.get("description")
        except:
            pass

    def finish_pytest_item(self, item):
        completed_at = time.time()
        self.result['time_ms'] = int((completed_at - self.result.get("started_at")) * 1000)
        self.result['completed_at'] = completed_at

        self.reporter.add_result(self.result, self.steps)

        self.result = {}  
        self.steps = {}

    def add_attachments(
            self, *files: Union[str, Tuple[str, str], Tuple[bytes, str, str]]
    ):
        if self.result:
            if self.step_uuid:
                attachments: list = self.steps[self.step_uuid].get("attachments", [])
                attachments.extend(files)
                self.steps[self.step_uuid]["attachments"] = attachments
            else:
                attachments: list = self.result.get("attachments", [])
                attachments.extend(files)
                self.result["attachments"] = attachments

    def load_run_from_lock(self):
        if QasePytestPlugin.meta_run_file.exists():
            with open(QasePytestPlugin.meta_run_file, "r") as lock_file:
                try:
                    self.run_id = int(lock_file.read())
                    self.reporter.set_run_id(self.run_id)
                except ValueError:
                    pass

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
