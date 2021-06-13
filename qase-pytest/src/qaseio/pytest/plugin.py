import logging
import pathlib
import time
from datetime import datetime
from typing import Tuple, Union

import pytest

import apitist
from filelock import FileLock

from qaseio.client import QaseApi
from qaseio.client.models import (
    TestRunCreate,
    TestRunInclude,
    TestRunInfo,
    TestRunResultCreate,
    TestRunResultStatus,
    TestRunResultStepCreate,
    TestRunResultUpdate,
)

QASE_MARKER = "qase"
PYTEST_TO_QASE_STATUS = {
    "PASSED": TestRunResultStatus.PASSED,
    "FAILED": TestRunResultStatus.FAILED,
    "SKIPPED": TestRunResultStatus.BLOCKED,
}


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


class QasePytestPlugin:
    testrun: TestRunInfo = None
    meta_run_file = pathlib.Path("qaseio.runid")

    def __init__(
        self,
        api_token,
        project,
        testrun=None,
        testplan=None,
        create_run=False,
        debug=False,
    ):
        self.client = QaseApi(api_token)
        self.project_code = project
        self.testrun_id = testrun
        self.testplan_id = testplan
        self.create_run = create_run
        self.debug = debug
        self.nodes_with_ids = {}
        self.cases_info = {}
        self.missing_ids = []
        self.existing_ids = []
        self.last_node = None
        self.project = self.client.projects.exists(self.project_code)
        self.comment = "Pytest Plugin Automation Run"
        if not self.project:
            raise ValueError("Unable to find given project code")
        self.check_testrun()
        if self.debug:
            logger = logging.getLogger(apitist.dist_name)
            logger.addHandler(logging.StreamHandler())
            logger.setLevel(logging.INFO)

    def pytest_report_header(self, config, startdir):
        """ Add extra-info in header """
        message = "qase: "
        if self.testrun_id:
            message += "existing testrun #{} selected".format(self.testrun_id)
        else:
            message += "a new testrun will be created"
        return message

    def check_case_ids(self, data):
        exist = []
        not_exist = []
        for _id in data.get("ids"):
            case = self.client.cases.exists(self.project_code, _id)
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
            testplan = self.client.plans.exists(
                self.project_code, self.testplan_id
            )
            if not testplan:
                raise ValueError("Could not find testplan")
            self.create_testrun([case.case_id for case in testplan.cases])
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
        if self.testrun_id and self.testrun is None:
            self.testrun = self.client.runs.exists(
                self.project_code,
                self.testrun_id,
                include=TestRunInclude.CASES,
            )

    def create_testrun(self, cases):
        if cases:
            self.testrun_id = self.client.runs.create(
                self.project_code,
                TestRunCreate(
                    "Automated Run {}".format(str(datetime.now())),
                    cases=cases,
                ),
            ).id
            print()
            print(
                "Qase TMS: created testrun "
                "https://app.qase.io/run/{}/dashboard/{}".format(
                    self.project_code, self.testrun_id
                )
            )

    def get_step_position(self, identifier: Union[int, str], case):
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

    def start_step(self, identifier):
        case_ids = self.nodes_with_ids[self.last_node].get("ids")
        if len(case_ids) > 1:
            # We could not match steps with more then one case
            raise MoreThenOneCaseIdException(
                "Test case decorated with several ids: {}".format(
                    ", ".join(case_ids)
                )
            )
        elif case_ids[0] in self.missing_ids:
            return None
        case = self.cases_info.get(case_ids[0])
        position = self.get_step_position(identifier, case)
        return position

    def finish_step(self, position: int, exception=None):
        if not position:
            return
        status = TestRunResultStatus.PASSED
        if exception:
            status = TestRunResultStatus.FAILED
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
            if self.meta_run_file.exists():
                with open(self.meta_run_file, "r") as lock_file:
                    try:
                        self.testrun_id = int(lock_file.read())
                    except ValueError:
                        pass
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

    @staticmethod
    def drop_run_id():
        if QasePytestPlugin.meta_run_file.exists():
            QasePytestPlugin.meta_run_file.unlink()

    def pytest_sessionfinish(self, session, exitstatus):
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
                    result(TestRunResultStatus.BLOCKED)
                else:
                    result(TestRunResultStatus.FAILED)
            elif report.skipped:
                if self.nodes_with_ids[item.nodeid]["result"] in (
                    None,
                    TestRunResultStatus.PASSED,
                ):
                    result("skipped")
            else:
                if self.nodes_with_ids[item.nodeid]["result"] is None:
                    result(TestRunResultStatus.PASSED)

    def start_pytest_item(self, item):
        if item.nodeid in self.nodes_with_ids:
            self.last_node = item.nodeid
            hashes = []
            for _id in self.nodes_with_ids[item.nodeid].get("ids", []):
                if _id not in self.missing_ids:
                    result = self.client.results.create(
                        self.project_code,
                        self.testrun_id,
                        TestRunResultCreate(
                            _id, TestRunResultStatus.IN_PROGRESS
                        ),
                    )
                    hashes.append(result.hash)
            self.nodes_with_ids[item.nodeid]["hashes"] = hashes
            self.nodes_with_ids[item.nodeid]["started_at"] = time.time()

    def finish_pytest_item(self, item):
        if item.nodeid in self.nodes_with_ids:
            results = self.nodes_with_ids[item.nodeid]
            hashes = results.get("hashes", [])
            attachments = results.get("attachments", [])
            steps = [
                TestRunResultStepCreate(position=pos, **values)
                for pos, values in results.get("steps", {}).items()
            ]
            attached = []
            if attachments:
                attached = self.client.attachments.upload(
                    self.project_code, *attachments
                )
            for hash in hashes:
                self.client.results.update(
                    self.project_code,
                    self.testrun_id,
                    hash,
                    TestRunResultUpdate(
                        status=results.get("result"),
                        comment=self.comment,
                        stacktrace=results.get("error"),
                        time_ms=int(
                            (time.time() - results.get("started_at")) * 1000
                        ),
                        attachments=[attach.hash for attach in attached],
                        steps=steps,
                    ),
                )
            self.last_node = None

    def add_attachments(
        self, *files: Union[str, Tuple[str, str], Tuple[bytes, str, str]]
    ):
        if self.last_node:
            node = self.nodes_with_ids[self.last_node]
            attachments: list = node.get("attachments", [])
            attachments.extend(files)
            node["attachments"] = attachments


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
