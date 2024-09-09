import logging
import os
import re
import uuid

from qase.commons import ConfigManager
from qase.commons.models import Result, Suite, Step, Field
from qase.commons.models.step import StepType, StepGherkinData
from qase.commons.reporters import QaseCoreReporter

from .plugin import QaseRuntimeSingleton
from .types import STATUSES
from .models import *

logger = logging.getLogger("qase-robotframework")


class Listener:
    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self):
        config = ConfigManager()
        self.reporter = QaseCoreReporter(config)
        self.runtime = QaseRuntimeSingleton.get_instance()
        self.step_uuid = None
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

    def start_suite(self, name, attributes):
        self.suite = {
            "title": name,
            "description": attributes["doc"]
        }

        logger.debug("Starting suite '%s'", name)

    def start_test(self, name, attributes: StartTestModel):
        logger.debug("Starting test '%s'", name)

        self.runtime.result = Result(title=name, signature=name)
        self.runtime.steps = {}

    def end_test(self, name, attributes: EndTestModel):
        logger.debug("Finishing test '%s'", name)

        self.step_uuid = None

        if self.__is_test_ignore(attributes.get("tags")):
            logger.info("Test '%s' is ignored", name)
            return

        case_id = self._extract_ids(attributes.get("tags"))
        if case_id:
            self.runtime.result.testops_id = int(case_id)

        self.runtime.result.execution.complete()
        self.runtime.result.execution.set_status(STATUSES[attributes.get("status")])
        self.runtime.result.execution.stacktrace = attributes.get("message")
        self.runtime.result.add_steps([step for key, step in self.runtime.steps.items()])

        self.runtime.result.add_field(Field("description", attributes.get("doc")))

        if self.suite:
            self.runtime.result.suite = Suite(self.suite.get("title"), self.suite.get("description"))

        if "source" in attributes:
            file_path = attributes["source"].split(os.getcwd() + os.path.sep)[1]
            signature = '::'.join(file_path.split(os.path.sep))
            if self.suite:
                signature += f"::{self.suite.get('title').lower().replace(' ', '_')}::{name.lower().replace(' ', '_')}"

            if self.runtime.result.testops_id:
                signature += f"::{self.runtime.result.testops_id}"

            self.runtime.result.signature = signature

        self.reporter.add_result(self.runtime.result)

        logger.info(
            "Finished case result: %s, error: %s",
            attributes.get("status"),
            attributes.get("message"),
        )

    def start_keyword(self, name, attributes):
        if attributes["type"] != "KEYWORD" or attributes["status"] == "NOT RUN":
            return

        id = str(uuid.uuid4())
        step = Step(
            step_type=StepType.GHERKIN,
            id=id,
            data=StepGherkinData(keyword=attributes["kwname"], name=name, line=attributes["lineno"])
        )

        self.runtime.add_step(step)
        self.step_uuid = id

    def end_keyword(self, name, attributes):
        if attributes["type"] != "KEYWORD" or attributes["status"] == "NOT RUN":
            return

        self.runtime.finish_step(self.step_uuid, STATUSES[attributes["status"]])
        self.step_uuid = self.runtime.steps[self.step_uuid].parent_id

    def end_suite(self, name, attributes: EndSuiteModel):
        self.suite = {}
        logger.debug("Finishing suite '%s'", name)

    def close(self):
        logger.info("complete run executing")
        self.reporter.complete_run()

    @staticmethod
    def log_message(message):
        logger.debug("Log:", message)

    @staticmethod
    def _extract_ids(list_of_tags: List[str]):
        qase_id = re.compile(r"Q-(\d+)", re.IGNORECASE)
        for tag in list_of_tags:
            if qase_id.fullmatch(tag):
                return int(qase_id.match(tag).groups()[0])
        return None

    @staticmethod
    def __is_test_ignore(list_of_tags: List[str]):
        return any(tag.lower() == "ignore" for tag in list_of_tags)
