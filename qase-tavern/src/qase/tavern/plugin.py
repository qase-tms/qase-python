import json
import uuid
import re

from qase.commons.models import Runtime, Result, Relation, Attachment
from qase.commons.models.relation import SuiteData
from qase.commons.models.step import Step, StepType, StepTextData


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
                self.runtime.result.execution.status = "failed"
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
        qase_id, title = self.extract_qase_id(self._get_title(item))
        self.runtime.result = Result(
            title=title,
            signature='',
        )
        if qase_id:
            self.runtime.result.testops_id = qase_id

        self._set_relations(item)
        self._set_steps(item)
        self._get_signature(item)

        # self._set_testops_id(item)

    @staticmethod
    def _get_title(item):
        if hasattr(item, "spec"):
            return item.spec["test_name"]

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
        self.runtime.result.signature = item.nodeid.replace("/", "::")
        if self.runtime.result.testops_id:
            self.runtime.result.signature += f"::{self.runtime.result.testops_id}"
        for key, val in self.runtime.result.params.items():
            self.runtime.result.signature += f"::{{{key}:{val}}}"

    @staticmethod
    def extract_qase_id(text):
        match = re.search(r'qaseid=\s*(\d+)', text, re.IGNORECASE)
        if match:
            qase_id = int(match.group(1))
            remaining_text = re.sub(r'qaseid=\s*\d+', '', text, flags=re.IGNORECASE).strip()
            return qase_id, remaining_text
        else:
            return None, text


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
