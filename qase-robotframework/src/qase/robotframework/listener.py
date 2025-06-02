import logging
import pathlib
import uuid

from filelock import FileLock
from qase.commons import ConfigManager
from qase.commons.models import Result, Step, Field, Relation
from qase.commons.models.relation import SuiteData
from qase.commons.models.step import StepType, StepGherkinData
from qase.commons.reporters import QaseCoreReporter
from robot.libraries.BuiltIn import BuiltIn
from qase.commons.utils import QaseUtils

from .filter import Filter
from .plugin import QaseRuntimeSingleton
from .tag_parser import TagParser
from .types import STATUSES
from .models import *

logger = logging.getLogger("qase-robotframework")


def get_pool_id():
    return BuiltIn().get_variable_value('${PABOTQUEUEINDEX}', None)


def get_last_level_flag():
    return BuiltIn().get_variable_value('${PABOTISLASTEXECUTIONINPOOL}', None)


class Listener:
    ROBOT_LISTENER_API_VERSION = 3

    meta_run_file = pathlib.Path("src.run")

    def __init__(self):
        config = ConfigManager()
        self.reporter = QaseCoreReporter(
            config, 'robotframework', 'qase-robotframework')
        self.runtime = QaseRuntimeSingleton.get_instance()
        self.tests = {}
        self.pabot_index = None
        self.last_level_flag = None

        if config.config.debug:
            logger.setLevel(logging.DEBUG)
            ch = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            ch.setFormatter(formatter)
            logger.addHandler(ch)

    def start_suite(self, suite, result):
        self.pabot_index = get_pool_id()
        self.last_level_flag = get_last_level_flag()
        if self.pabot_index is not None:
            try:
                if int(self.pabot_index) == 0:
                    test_run_id = self.reporter.start_run()
                    with FileLock("qase.lock"):
                        if test_run_id:
                            with open(self.meta_run_file, "w") as lock_file:
                                lock_file.write(str(test_run_id))
                else:
                    while True:
                        if Listener.meta_run_file.exists():
                            self.__load_run_from_lock()
                            break
            except RuntimeError:
                logger.error("Failed to create or read lock file")
        else:
            self.reporter.start_run()

        execution_plan = self.reporter.get_execution_plan()
        if execution_plan:
            selector = Filter(*execution_plan)
            suite.visit(selector)

        self.tests.update(self.__extract_tests_with_suites(suite))

    def start_test(self, test, result):
        logger.debug("Starting test '%s'", test.name)

        self.runtime.result = Result(title=test.name, signature=test.name)
        self.runtime.steps = {}

    def end_test(self, test, result):
        logger.debug("Finishing test '%s'", test.name)

        test_metadata = TagParser.parse_tags(test.tags)

        if test_metadata.ignore:
            logger.info("Test '%s' is ignored", test.name)
            return

        if test_metadata.qase_ids:
            self.runtime.result.testops_ids = test_metadata.qase_ids

        self.runtime.result.execution.complete()
        self.runtime.result.execution.set_status(STATUSES[result.status])
        if hasattr(result, 'message'):
            self.runtime.result.execution.stacktrace = result.message

        steps = self.__parse_steps(result)
        self.runtime.result.add_steps(steps)

        if len(test_metadata.params) > 0:
            params: dict = {}
            for param in test_metadata.params:
                params[param] = BuiltIn().get_variable_value(f"${{{param}}}")
            self.runtime.result.params = params

        if hasattr(test, "doc"):
            self.runtime.result.add_field(Field("description", test.doc))

        if test_metadata.fields:
            for key, value in test_metadata.fields.items():
                self.runtime.result.add_field(Field(key, value))

        suites = self.tests.get(f"{test.name}:{test.lineno}")
        if suites:
            relations = Relation()
            for suite in suites:
                relations.add_suite(SuiteData(suite))
            self.runtime.result.relations = relations

            self.runtime.result.signature = QaseUtils.get_signature(
                self.runtime.result.testops_ids,
                [suite.lower().replace(" ", "_") for suite in suites] +
                [test.name.lower().replace(" ", "_")],
                self.runtime.result.params
            )

        self.reporter.add_result(self.runtime.result)

        logger.info(
            "Finished case result: %s, error: %s",
            result.status,
            hasattr(result, "message") and result.message or None,
        )

    def close(self):
        if self.last_level_flag is not None:
            if int(self.last_level_flag) == 1:
                Listener.drop_run_id()
            else:
                self.reporter.complete_worker()

        if not Listener.meta_run_file.exists():
            logger.info("complete run executing")
            self.reporter.complete_run()

    def __extract_tests_with_suites(self, suite, parent_suites=None):
        if parent_suites is None:
            parent_suites = []

        current_suites = parent_suites + [suite.name]

        test_dict = {}

        if hasattr(suite, 'suites') and suite.suites:
            for sub_suite in suite.suites:
                test_dict.update(self.__extract_tests_with_suites(
                    sub_suite, current_suites))

        if hasattr(suite, 'tests') and suite.tests:
            for test in suite.tests:
                test_key = f"{test.name}:{test.lineno}"
                test_dict[test_key] = current_suites

        return test_dict

    def __parse_steps(self, result) -> List[Step]:
        steps = []

        for i in range(len(result.body)):
            if hasattr(result.body[i], "type") and result.body[i].type == "MESSAGE":
                continue

            if hasattr(result.body[i], "type") and result.body[i].type == "IF/ELSE ROOT":
                condition_steps = self.__parse_condition_steps(result.body[i])
                for step in condition_steps:
                    steps.append(step)
                continue

            if hasattr(result.body[i], "type") and result.body[i].type != "KEYWORD":
                step_name = result.body[i].type
                if hasattr(result.body[i], "values"):
                    step_name += " " + " ".join(result.body[i].values)
            else:
                step_name = result.body[i].name

            step = Step(
                step_type=StepType.GHERKIN,
                id=str(uuid.uuid4()),
                data=StepGherkinData(keyword=step_name, name=step_name, line=0)
            )

            step.execution.set_status(STATUSES[result.body[i].status])
            step.execution.start_time = result.body[i].start_time.timestamp()
            step.execution.duration = result.body[i].elapsed_time.microseconds
            step.execution.end_time = result.body[i].end_time.timestamp()

            if hasattr(result.body[i], "body"):
                step.steps = self.__parse_steps(result.body[i])

            steps.append(step)

        return steps

    def __parse_condition_steps(self, result_step) -> List[Step]:
        steps = []

        for body_element in result_step.body:
            if hasattr(body_element, "type"):
                step = Listener._create_gherkin_step_with_type(body_element)
                child_steps = self.__parse_steps(body_element)

                Listener._set_step_status_based_on_children(step, child_steps)
                step.steps = child_steps
            else:
                step = Listener._create_gherkin_step_from_name(body_element)

            step.execution.start_time = None
            step.execution.end_time = None

            steps.append(step)

        return steps

    @staticmethod
    def _create_gherkin_step_with_type(body_element) -> Step:
        """Create a Gherkin step from a body element with type attribute."""
        step = Step(
            step_type=StepType.GHERKIN,
            id=str(uuid.uuid4()),
            data=StepGherkinData(
                keyword=body_element.type,
                name=body_element.type,
                line=0
            )
        )

        return step

    @staticmethod
    def _create_gherkin_step_from_name(body_element) -> Step:
        """Create a Gherkin step from a body element with name attribute."""
        step = Step(
            step_type=StepType.GHERKIN,
            id=str(uuid.uuid4()),
            data=StepGherkinData(
                keyword=body_element.name,
                name=body_element.name,
                line=0
            )
        )

        return step

    @staticmethod
    def _set_step_status_based_on_children(step: Step, child_steps: List[Step]) -> None:
        """Set the status of a step based on its children's statuses."""
        if all(s.execution.status == "skipped" for s in child_steps):
            step.execution.set_status("skipped")
        else:
            step.execution.set_status("passed")

    def __load_run_from_lock(self):
        if Listener.meta_run_file.exists():
            with open(Listener.meta_run_file, "r") as lock_file:
                try:
                    test_run_id = str(lock_file.read())
                    self.reporter.set_run_id(test_run_id)
                except ValueError:
                    pass

    @staticmethod
    def drop_run_id():
        if Listener.meta_run_file.exists():
            Listener.meta_run_file.unlink()
