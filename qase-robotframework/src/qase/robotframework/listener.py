import logging
import uuid

from qase.commons import ConfigManager
from qase.commons.models import Result, Suite, Step, Field
from qase.commons.models.step import StepType, StepGherkinData
from qase.commons.reporters import QaseCoreReporter

from .plugin import QaseRuntimeSingleton
from .tag_parser import TagParser
from .types import STATUSES
from .models import *

logger = logging.getLogger("qase-robotframework")


class Listener:
    ROBOT_LISTENER_API_VERSION = 3

    def __init__(self):
        config = ConfigManager()
        self.reporter = QaseCoreReporter(config)
        self.runtime = QaseRuntimeSingleton.get_instance()
        self.step_uuid = None
        self.tests = {}
        self.suite = {}

        if config.config.debug:
            logger.setLevel(logging.DEBUG)
            ch = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            ch.setFormatter(formatter)
            logger.addHandler(ch)

        self.reporter.start_run()

    def start_suite(self, suite, result):
        self.tests.update(self.__extract_tests_with_suites(suite))

    def start_test(self, test, result):
        logger.debug("Starting test '%s'", test.name)

        self.runtime.result = Result(title=test.name, signature=test.name)
        self.runtime.steps = {}

    def end_test(self, test, result):
        logger.debug("Finishing test '%s'", test.name)

        self.step_uuid = None

        test_metadata = TagParser.parse_tags(test.tags)

        if test_metadata.ignore:
            logger.info("Test '%s' is ignored", test.name)
            return

        if test_metadata.qase_id:
            self.runtime.result.testops_id = int(test_metadata.qase_id)

        self.runtime.result.execution.complete()
        self.runtime.result.execution.set_status(STATUSES[result.status])
        if hasattr(result, 'message'):
            self.runtime.result.execution.stacktrace = result.message

        steps = self.__parse_steps(test, result)
        self.runtime.result.add_steps(steps)

        if hasattr(test, "doc"):
            self.runtime.result.add_field(Field("description", test.doc))

        if test_metadata.fields:
            for key, value in test_metadata.fields.items():
                self.runtime.result.add_field(Field(key, value))

        suites = self.tests.get(f"{test.name}:{test.lineno}")
        if suites:
            self.runtime.result.suite = Suite('\t'.join(suites), "")
            signature = "::".join(
                suite.lower().replace(" ", "_") for suite in suites) + f"::{test.name.lower().replace(' ', '_')}"

            if self.runtime.result.testops_id:
                signature += f"::{self.runtime.result.testops_id}"

            self.runtime.result.signature = signature

        self.reporter.add_result(self.runtime.result)

        logger.info(
            "Finished case result: %s, error: %s",
            result.status,
            hasattr(result, "message") and result.message or None,
        )

    def close(self):
        logger.info("complete run executing")
        self.reporter.complete_run()

    def __extract_tests_with_suites(self, suite, parent_suites=None):
        if parent_suites is None:
            parent_suites = []

        current_suites = parent_suites + [suite.name]

        test_dict = {}

        if hasattr(suite, 'suites') and suite.suites:
            for sub_suite in suite.suites:
                test_dict.update(self.__extract_tests_with_suites(sub_suite, current_suites))

        if hasattr(suite, 'tests') and suite.tests:
            for test in suite.tests:
                test_key = f"{test.name}:{test.lineno}"
                test_dict[test_key] = current_suites

        return test_dict

    def __parse_steps(self, test, result) -> List[Step]:
        steps = []

        for i in range(len(result.body)):
            if hasattr(test.body[i], "type") and test.body[i].type == "IF/ELSE ROOT":
                condition_steps = self.__parse_condition_steps(test.body[i], result.body[i])
                for step in condition_steps:
                    steps.append(step)
                continue

            step = Step(
                step_type=StepType.GHERKIN,
                id=str(uuid.uuid4()),
                data=StepGherkinData(keyword=test.body[i].name, name=test.body[i].name, line=test.body[i].lineno)
            )

            step.execution.set_status(STATUSES[result.body[i].status])
            step.execution.start_time = result.body[i].start_time.timestamp()
            step.execution.duration = result.body[i].elapsed_time.microseconds

            steps.append(step)

        return steps

    def __parse_condition_steps(self, test_step, result_step) -> List[Step]:
        steps = []
        for i in range(len(result_step.body)):
            if hasattr(result_step.body[i], "type"):
                step = Step(
                    step_type=StepType.GHERKIN,
                    id=str(uuid.uuid4()),
                    data=StepGherkinData(keyword=test_step.body[i].type, name=test_step.body[i].type,
                                         line=test_step.body[i].lineno)
                )
                step.execution.start_time = None
                child_steps = self.__parse_steps(test_step.body[i], result_step.body[i])

                if all(s.execution.status == "skipped" for s in child_steps):
                    step.execution.set_status("skipped")
                else:
                    step.execution.set_status("passed")

                step.steps = child_steps
                steps.append(step)
                continue

            step = Step(
                step_type=StepType.GHERKIN,
                id=str(uuid.uuid4()),
                data=StepGherkinData(keyword=test_step.body[i].name, name=test_step.body[i].name,
                                     line=test_step.body[i].lineno)
            )
            steps.append(step)

        return steps
