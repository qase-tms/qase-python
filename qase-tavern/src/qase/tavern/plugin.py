import json
import uuid
import re
from typing import Tuple, List

from qase.commons.models import Runtime, Result, Relation, Attachment
from qase.commons.models.relation import SuiteData
from qase.commons.models.step import Step, StepType, StepTextData
from qase.commons.utils import QaseUtils


class QasePytestPlugin:

    def __init__(
            self,
            reporter
    ):
        self.runtime = Runtime()
        self.reporter = reporter
        self.config = reporter.config
        self.run_id = None
        self._current_item = None
        self.ignore = None

    def pytest_sessionstart(self, session):
        self.run_id = self.reporter.start_run()

    def pytest_sessionfinish(self, session, exitstatus):
        self.reporter.complete_worker()
        self.reporter.complete_run()

    def pytest_runtest_protocol(self, item):
        self.start_pytest_item(item)

    def pytest_runtest_makereport(self, item, call):
        if call.when == "call":
            if call.excinfo:
                # Determine if it's an assertion error or other error
                is_assertion_error = call.excinfo.typename == "AssertionError"
                status = "failed" if is_assertion_error else "invalid"
                self.runtime.result.execution.status = status
                if hasattr(call.excinfo, "value"):
                    self.runtime.result.execution.stacktrace = '\n'.join(call.excinfo.value.args)
                    if hasattr(call.excinfo.value, "failures"):
                        self.runtime.result.message = '\n'.join(call.excinfo.value.failures)

                    if hasattr(call.excinfo.value, "stage"):
                        failed_step = call.excinfo.value.stage['name']

                        is_failed = False
                        for key, step in self.runtime.steps.items():
                            step.execution.complete()
                            if step.data.action == failed_step:
                                step.execution.set_status("failed")
                                is_failed = True
                                continue

                            if is_failed:
                                step.execution.set_status("skipped")
                                continue

                            step.execution.set_status("passed")
                        return

                    for key, step in self.runtime.steps.items():
                        step.execution.complete()
                        step.execution.set_status("skipped")

                return

            self.runtime.result.execution.status = "passed"
            for key, step in self.runtime.steps.items():
                step.execution.complete()
                step.execution.set_status("passed")

    def pytest_runtest_logfinish(self):
        self.runtime.result.execution.complete()
        self.runtime.result.steps = [step for key, step in self.runtime.steps.items()]
        self.reporter.add_result(self.runtime.result)
        self.runtime.clear()

    def start_pytest_item(self, item):
        qase_ids, project_ids, title = self.extract_qase_ids(self._get_title(item))
        self.runtime.result = Result(
            title=title,
            signature='',
        )
        if project_ids:
            # Multi-project mode: set project mapping
            for project_code, testops_ids in project_ids.items():
                self.runtime.result.set_testops_project_mapping(project_code, testops_ids)
        elif qase_ids:
            # Single project mode: use old testops_ids
            self.runtime.result.testops_ids = qase_ids

        self._set_relations(item)
        self._set_steps(item)
        self._get_signature(item)

    @staticmethod
    def _get_title(item):
        if hasattr(item, "spec"):
            return item.spec["test_name"]
        return ""

    def _set_relations(self, item):
        if hasattr(item, "fspath") and hasattr(item.fspath, "basename"):
            self.runtime.result.relations = self.__prepare_relations([item.fspath.basename])

    @staticmethod
    def __prepare_relations(suites: []):
        relation = Relation()

        for suite in suites:
            relation.add_suite(SuiteData(title=suite))

        return relation

    def _set_steps(self, item):
        if hasattr(item, "spec"):
            for stage in item.spec['stages']:
                self.runtime.add_step(self.__prepare_step(stage))

    @staticmethod
    def __prepare_step(stage) -> Step:
        data = StepTextData(stage['name'])
        step = Step(StepType.TEXT, str(uuid.uuid4()), data)

        step.attachments.append(
            Attachment(file_name='request.json', content=json.dumps(stage['request']), mime_type='application/json',
                       temporary=True))
        step.attachments.append(
            Attachment(file_name='response.json', content=json.dumps(stage['response']), mime_type='application/json',
                       temporary=True))

        return step

    def _get_signature(self, item):
        self.runtime.result.signature = QaseUtils.get_signature(
            self.runtime.result.testops_ids,
            [suite.title for suite in self.runtime.result.relations.suite.data] + [self._get_title(item)],
            self.runtime.result.params
        )

    @staticmethod
    def extract_qase_ids(text) -> Tuple[List[int], dict, str]:
        if not isinstance(text, str):
            raise ValueError(f"Expected a string, but got {type(text).__name__}: {repr(text)}")

        project_ids = {}
        remaining_text = text

        # Extract project IDs: QaseProjectID.PROJ1=123,124 or QaseProjectID.PROJ1=123
        project_pattern = r'QaseProjectID\.([A-Za-z0-9_]+)=\s*([\d,]+)'
        project_matches = re.finditer(project_pattern, text, re.IGNORECASE)
        for match in project_matches:
            project_code = match.group(1)
            ids_str = match.group(2)
            testops_ids = [int(qid.strip()) for qid in ids_str.split(',') if qid.strip()]
            if project_code and testops_ids:
                project_ids[project_code] = testops_ids
            # Remove from text
            remaining_text = re.sub(re.escape(match.group(0)), '', remaining_text, flags=re.IGNORECASE)

        # Extract single project IDs: QaseID=123,124 (only if no project_ids found)
        qase_ids = []
        if not project_ids:
            match = re.search(r'QaseID=\s*([\d,]+)', remaining_text, re.IGNORECASE)
            if match:
                qase_ids = [int(qid) for qid in match.group(1).split(',')]
                remaining_text = re.sub(r'QaseID=\s*[\d,]+', '', remaining_text, flags=re.IGNORECASE)

        remaining_text = remaining_text.strip()

        return qase_ids, project_ids, remaining_text


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
