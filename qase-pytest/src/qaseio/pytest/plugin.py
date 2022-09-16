import logging
import pathlib
import time
from datetime import datetime
from typing import Tuple, Union
import platform
import sys
import pip
from pkg_resources import DistributionNotFound, get_distribution
import pytest

import apitist
from filelock import FileLock

from qaseio.api_client import ApiClient
from qaseio.configuration import Configuration
from qaseio.api.attachments_api import AttachmentsApi
from qaseio.api.cases_api import CasesApi
from qaseio.api.plans_api import PlansApi
from qaseio.api.projects_api import ProjectsApi
from qaseio.api.results_api import ResultsApi
from qaseio.api.runs_api import RunsApi
from qaseio.model.run_create import RunCreate
from qaseio.model.result_create_bulk import ResultCreateBulk
from qaseio.model.result_create_steps_inner import ResultCreateStepsInner
from qaseio.rest import ApiException


QASE_MARKER = "qase"

PYTEST_TO_QASE_STATUS = {
    "PASSED": 'passed',
    "FAILED": 'failed',
    "SKIPPED": 'skipped',
    "BLOCKED": 'blocked',
}


try:
    from xdist import is_xdist_master
except ImportError:

    def is_xdist_master(*args, **kwargs):
        return True


def package_version(name):
    try:
        version = get_distribution(name).version
    except DistributionNotFound:
        version = "unknown"
    return version


def get_ids_from_pytest_nodes(items):
    """Return tuple with item and test case ids for it and tests missing ids"""
    return (
        {
            item.nodeid: {
                "ids": item.get_closest_marker(QASE_MARKER).kwargs.get("ids")
            }
            for item in items
            if item.get_closest_marker(QASE_MARKER)
        },
        [item for item in items if not item.get_closest_marker(QASE_MARKER)],
    )


class MoreThenOneCaseIdException(Exception):
    pass


class MissingStepIdentifierException(Exception):
    pass


def get_step_position(identifier: Union[int, str], case):
    if isinstance(identifier, int):
        # We expect that this is correct position id
        return identifier
    if isinstance(identifier, str):
        # Trying to guess that identifier is hash or step name
        for pos, step in enumerate(case.steps):
            if identifier in (step.get("hash"), step.get("action")):
                return pos + 1
    raise MissingStepIdentifierException(
        "Missing step for identifier {}".format(identifier)
    )


def get_platform():
    platform_data = {
        'os': platform.system(),
        'arch': platform.machine(),
        'python': '.'.join(map(str, sys.version_info)),
        'pip': pip.__version__
    }
    return ';'.join([f'{key}={value}' for key, value in platform_data.items()])


def get_client():
    client_data = {
        'qaseapi': package_version('qaseio'),
        'qase-pytest': package_version('qase-pytest'),
        'pytest': pytest.__version__,
    }
    return ';'.join([f'{key}={value}' for key, value in client_data.items()])


class QasePytestPlugin:
    testrun = None
    meta_run_file = pathlib.Path("src.runid")

    def __init__(
            self,
            api_token,
            project,
            testrun=None,
            testplan=None,
            create_run=False,
            complete_run=False,
            debug=False,
    ):
        configuration = Configuration()
        configuration.api_key['TokenAuth'] = api_token
        self.client = ApiClient(configuration)
        self.client.set_default_header('X-Platform', get_platform())
        self.client.set_default_header('X-Client', get_client())
        self.project_code = project
        self.testrun_id = int(testrun)
        self.testplan_id = int(testplan)
        self.create_run = create_run
        self.complete_run = complete_run
        self.debug = debug
        self.nodes_with_ids = {}
        self.results_for_send = {}
        self.cases_info = {}
        self.missing_ids = []
        self.existing_ids = []
        self.last_node = None
        self.project = self.get_project(self.project_code)
        self.comment = "Pytest Plugin Automation Run"
        self.check_testrun()
        if self.debug:
            logger = logging.getLogger(apitist.dist_name)
            logger.addHandler(logging.StreamHandler())
            logger.setLevel(logging.INFO)

    def pytest_report_header(self, config, startdir):
        """ Add extra-info in header """
        message = "qase: "
        if self.testrun_id:
            message += "existing test run #{} selected".format(self.testrun_id)
        else:
            message += "a new test run will be created"
        return message

    def get_project(self, project_code):
        api_instance = ProjectsApi(self.client)
        try:
            response = api_instance.get_project(project_code)
            if hasattr(response, 'result'):
                return response.result
            raise ValueError("Unable to find given project code")
        except ApiException as e:
            print("Exception when calling ProjectApi->get_project: %s\n" % e)

    def check_case_ids(self, data):
        api_instance = CasesApi(self.client)
        exist = []
        not_exist = []
        for _id in data.get("ids"):
            case = api_instance.get_case(self.project_code, _id).result
            if case:
                self.cases_info[case.id] = case
                exist.append(_id)
                continue
            not_exist.append(_id)
        return exist, not_exist

    def get_missing_in_testrun(self, data):
        missing = []
        for _id in data.get("ids"):
            if _id not in self.testrun.cases:
                missing.append(_id)
        return missing

    def check_testrun(self):
        if (self.testrun_id or self.create_run) and self.testplan_id:
            raise ValueError(
                "You should provide either use testrun or testplan"
            )
        if self.testplan_id:
            api_plans = PlansApi(self.client)
            test_plan = api_plans.get_plan(
                self.project_code, self.testplan_id
            )
            if not test_plan:
                raise ValueError("Could not find test plan")
            self.create_testrun([case.case_id for case in test_plan.cases])
        self.load_testrun()
        if not self.testrun and not self.create_run:
            raise ValueError(
                "Unable to find given testrun id, you should specify it"
            )
        if self.testrun and self.create_run:
            raise ValueError(
                "You should provide either testrun/testplan id or "
                "select to create it, not both of it"
            )

    def load_testrun(self):
        api_runs = RunsApi(self.client)
        if self.testrun_id and self.testrun is None:
            self.testrun = api_runs.get_run(
                code=self.project_code,
                id=self.testrun_id,
                include='cases',
            ).result

    def create_testrun(self, cases):
        api_runs = RunsApi(self.client)
        if cases:
            result = api_runs.create_run(
                code=self.project_code,
                run_create=RunCreate(
                    title="Automated Run {}".format(str(datetime.now())),
                    cases=cases,
                    is_autotest=True
                ),
            )
            self.testrun_id = result.result.id
            print()
            print(
                "Qase TMS: created testrun "
                "https://app.qase.io/run/{}/dashboard/{}".format(
                    self.project_code, self.testrun_id
                )
            )

    def start_step(self, identifier):
        case_ids = self.nodes_with_ids[self.last_node].get("ids")
        if len(case_ids) > 1:
            # We could not match steps with more than one case
            raise MoreThenOneCaseIdException(
                "Test case decorated with several ids: {}".format(
                    ", ".join(case_ids)
                )
            )
        elif case_ids[0] in self.missing_ids:
            return None
        case = self.cases_info.get(case_ids[0])
        position = get_step_position(identifier, case)
        return position

    def finish_step(self, position: int, exception=None):
        if not position:
            return
        status = PYTEST_TO_QASE_STATUS['PASSED']
        if exception:
            status = PYTEST_TO_QASE_STATUS['FAILED']
        steps = self.nodes_with_ids[self.last_node].get("steps", {})
        steps[position] = {}
        steps[position]["status"] = status
        self.nodes_with_ids[self.last_node]["steps"] = steps

    @pytest.hookimpl(trylast=True)
    def pytest_collection_modifyitems(self, session, config, items):
        """
        Load list of items,
        check whether given ids for tests exist on server or not.

        Prints additional info at start of the run, if debug in True
        """
        with FileLock("qaseio.lock"):
            self.load_run_from_lock()
            self.load_testrun()
            self.nodes_with_ids, no_ids = get_ids_from_pytest_nodes(items)
            write_lines = []
            if no_ids:
                line = ", ".join([miss.name for miss in no_ids])
                write_lines.append(
                    "This tests does not have test case ids:\n" + line
                )

            for nodeid, data in self.nodes_with_ids.items():
                exist_ids, missing_ids = self.check_case_ids(data)
                if missing_ids:
                    write_lines.append(
                        "For test {} can't find test cases in TMS: {}".format(
                            nodeid, ", ".join([str(i) for i in missing_ids])
                        )
                    )

                if not self.create_run:
                    missing_in_run = self.get_missing_in_testrun(data)
                    if missing_in_run:
                        write_lines.append(
                            "For test {} could not find "
                            "test cases in run: {}".format(
                                nodeid,
                                ", ".join([str(i) for i in missing_in_run]),
                            )
                        )
                    self.missing_ids.extend(missing_in_run)
                self.missing_ids.extend(missing_ids)
                self.existing_ids.extend(exist_ids)

            if self.create_run and self.existing_ids and not self.testrun_id:
                self.create_testrun(self.existing_ids)
                self.load_testrun()

                with open(self.meta_run_file, "w") as lock_file:
                    lock_file.write(str(self.testrun_id))

        if write_lines and self.debug:
            writer = config.pluginmanager.get_plugin("terminalreporter")
            print()
            writer.ensure_newline()
            writer.section("Qase TMS", sep="=")
            for line in write_lines:
                writer.line(line)
            writer.section("Qase TMS setup finished", sep="=")

    def load_run_from_lock(self):
        if self.meta_run_file.exists():
            with open(self.meta_run_file, "r") as lock_file:
                try:
                    self.testrun_id = int(lock_file.read())
                except ValueError:
                    pass

    @staticmethod
    def drop_run_id():
        if QasePytestPlugin.meta_run_file.exists():
            QasePytestPlugin.meta_run_file.unlink()

    def pytest_sessionstart(self, session):
        if is_xdist_master(session):
            QasePytestPlugin.drop_run_id()

    def pytest_sessionfinish(self, session, exitstatus):
        if is_xdist_master(session):
            self.send_bulk_results()
            if self.complete_run:
                self.load_run_from_lock()
                self.complete()
            QasePytestPlugin.drop_run_id()

    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_protocol(self, item):
        self.start_pytest_item(item)
        yield
        self.finish_pytest_item(item)

    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_makereport(self, item, call):
        report = (yield).get_result()

        if item.nodeid in self.nodes_with_ids:

            def result(res):
                self.nodes_with_ids[item.nodeid]["result"] = res

            if report.longrepr:
                self.nodes_with_ids[item.nodeid]["error"] = report.longreprtext

            # Defining test result
            if report.when == "setup":
                result(None)

            if report.failed:
                if call.excinfo.typename != "AssertionError":
                    result(PYTEST_TO_QASE_STATUS['BLOCKED'])
                else:
                    result(PYTEST_TO_QASE_STATUS['FAILED'])
            elif report.skipped:
                if self.nodes_with_ids[item.nodeid]["result"] in (
                        None,
                        PYTEST_TO_QASE_STATUS['PASSED'],
                ):
                    result(PYTEST_TO_QASE_STATUS['SKIPPED'])
            else:
                if self.nodes_with_ids[item.nodeid]["result"] is None:
                    result(PYTEST_TO_QASE_STATUS['PASSED'])

    def start_pytest_item(self, item):
        if item.nodeid in self.nodes_with_ids:
            self.last_node = item.nodeid
            for _id in self.nodes_with_ids[item.nodeid].get("ids", []):
                if _id not in self.missing_ids:
                    self.results_for_send[_id] = {
                        'case_id': _id,
                        'status': 'in_progress',
                        'is_api_result': True,
                    }
            self.nodes_with_ids[item.nodeid]["started_at"] = time.time()

    def finish_pytest_item(self, item):
        if item.nodeid in self.nodes_with_ids:
            results = self.nodes_with_ids[item.nodeid]
            attachments = results.get("attachments", [])
            steps = [
                ResultCreateStepsInner(position=pos, **values)
                for pos, values in results.get("steps", {}).items()
            ]
            attached = []
            api_attachments = AttachmentsApi(self.client)
            if attachments:
                attached = api_attachments.upload_attachment(
                    self.project_code, **attachments
                ).result
            for _id in self.nodes_with_ids[item.nodeid].get("ids", []):
                if _id in self.results_for_send:
                    self.results_for_send[_id]['status'] = results.get("result")
                    self.results_for_send[_id]['comment'] = self.comment
                    self.results_for_send[_id]['stacktrace'] = results.get("error")
                    self.results_for_send[_id]['time_ms'] = int(
                                (time.time() - results.get("started_at")) * 1000
                            )
                    self.results_for_send[_id]['attachments'] = [attach.hash for attach in attached]
                    self.results_for_send[_id]['steps'] = steps
            self.last_node = None

    def add_attachments(
            self, *files: Union[str, Tuple[str, str], Tuple[bytes, str, str]]
    ):
        if self.last_node:
            node = self.nodes_with_ids[self.last_node]
            attachments: list = node.get("attachments", [])
            attachments.extend(files)
            node["attachments"] = attachments

    def send_bulk_results(self):
        api_results = ResultsApi(self.client)
        print()
        print(f"Sending results to test run {self.testrun_id}...")
        print(type(self.testrun_id))
        try:
            api_results.create_result_bulk(
                code=self.project_code,
                id=self.testrun_id,
                result_create_bulk=ResultCreateBulk(
                    results=list(self.results_for_send.values())
                )
            )
            print(f"Results of run {self.testrun_id} was sent")
        except Exception as e:
            print(f"Error at sending results for run {self.testrun_id}: {e}")

    def complete(self):
        if self.testrun_id and self.complete_run:
            api_runs = RunsApi(self.client)
            print()
            print(f"Finishing run {self.testrun_id}")
            res = api_runs.get_run(self.project_code, self.testrun_id).result
            if res.status == 1:
                print(f"Run {self.testrun_id} already finished")
                return
            try:
                api_runs.complete_run(self.project_code, self.testrun_id)
                print(f"Run {self.testrun_id} was finished successfully")
            except Exception as e:
                print(f"Run {self.testrun_id} was finished with error: {e}")


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
            raise Exception("Init plugin first")
        return QasePytestPluginSingleton._instance

    def __init__(self):
        """ Virtually private constructor"""
        raise Exception("Use get_instance()")
