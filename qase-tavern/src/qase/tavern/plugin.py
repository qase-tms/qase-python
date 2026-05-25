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
        self._tavern_stage_index = 0

    def pytest_sessionstart(self, session):
        self.run_id = self.reporter.start_run()

    def pytest_sessionfinish(self, session, exitstatus):
        self.reporter.complete_worker()
        self.reporter.complete_run()

    def pytest_runtest_protocol(self, item):
        self.start_pytest_item(item)

    def pytest_tavern_beta_before_every_request(self, request_args):
        """Mark the actual start time of the current Tavern stage.

        Each stage triggers exactly one ``before_every_request`` call, so
        we use the current stage index as a cursor into ``runtime.steps``.
        """
        if self.runtime.result is None:
            return
        steps_list = list(self.runtime.steps.values())
        if self._tavern_stage_index < len(steps_list):
            steps_list[self._tavern_stage_index].execution.start_time = QaseUtils.get_real_time()

    def pytest_tavern_beta_after_every_response(self, expected, response):
        """Mark the actual end time of the current Tavern stage and advance."""
        if self.runtime.result is None:
            return
        steps_list = list(self.runtime.steps.values())
        if self._tavern_stage_index < len(steps_list):
            steps_list[self._tavern_stage_index].execution.complete()
            self._tavern_stage_index += 1

    def pytest_runtest_makereport(self, item, call):
        if self.runtime.result is None:
            return
        if call.when == "call":
            if call.excinfo:
                # Determine if it's an assertion error or other error
                is_assertion_error = call.excinfo.typename == "AssertionError"
                status = "failed" if is_assertion_error else "invalid"
                self.runtime.result.execution.status = status
                if hasattr(call.excinfo, "value"):
                    self.runtime.result.execution.stacktrace = '\n'.join(str(a) for a in call.excinfo.value.args)
                    if hasattr(call.excinfo.value, "failures"):
                        self.runtime.result.message = '\n'.join(call.excinfo.value.failures)

                    if hasattr(call.excinfo.value, "stage"):
                        failed_step = call.excinfo.value.stage['name']

                        is_failed = False
                        for key, step in self.runtime.steps.items():
                            if step.data.action == failed_step:
                                self._ensure_step_closed(step, "failed")
                                is_failed = True
                                continue

                            if is_failed:
                                self._ensure_step_closed(step, "skipped")
                                continue

                            self._ensure_step_closed(step, "passed")
                        return

                    for key, step in self.runtime.steps.items():
                        self._ensure_step_closed(step, "skipped")

                return

            self.runtime.result.execution.status = "passed"
            for key, step in self.runtime.steps.items():
                self._ensure_step_closed(step, "passed")

    @staticmethod
    def _ensure_step_closed(step, status):
        """Close a step without overwriting timings already set by Tavern hooks.

        ``pytest_tavern_beta_after_every_response`` calls ``complete()`` for
        every stage that actually ran, so we must not stamp the test-end
        time on top of that. Steps that never executed (skipped after a
        failure, or no hook fired) get a zero-duration placeholder at
        ``now`` so the timeline doesn't show them spanning the full test.
        """
        if not step.execution.end_time:
            if status == "skipped":
                now = QaseUtils.get_real_time()
                step.execution.start_time = now
                step.execution.end_time = now
                step.execution.duration = 0
            else:
                step.execution.complete()
        step.execution.set_status(status)

    def pytest_runtest_logfinish(self):
        if self.runtime.result is None:
            return
        self.runtime.result.execution.complete()
        self.runtime.result.steps = [step for key, step in self.runtime.steps.items()]
        self.reporter.add_result(self.runtime.result)
        self.runtime.clear()

    def start_pytest_item(self, item):
        self._tavern_stage_index = 0
        qase_ids, project_ids, title, tags = self.extract_qase_ids(self._get_title(item))
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

        if tags:
            self.runtime.result.add_tags(tags)

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

        step.add_attachment(
            Attachment(file_name='request.json', content=json.dumps(stage['request']), mime_type='application/json',
                       temporary=True))
        step.add_attachment(
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
    def extract_qase_ids(text) -> Tuple[List[int], dict, str, List[str]]:
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

        # Extract tags: QaseTags.tag1,tag2
        tags = []
        tag_match = re.search(r'QaseTags\.([\w,]+)', remaining_text, re.IGNORECASE)
        if tag_match:
            tags = [t.strip() for t in tag_match.group(1).split(',') if t.strip()]
            remaining_text = re.sub(re.escape(tag_match.group(0)), '', remaining_text, flags=re.IGNORECASE)

        remaining_text = remaining_text.strip()

        return qase_ids, project_ids, remaining_text, tags


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
