import configparser
import logging
import os
import re
import sys
from datetime import datetime
from enum import Enum
from pkg_resources import DistributionNotFound, get_distribution
from typing import List, Optional

from qaseio import client
from qaseio.client.models import (
    TestCaseInfo,
    TestRunCreate,
    TestRunResultCreate,
    TestRunResultStatus,
    TestRunResultStepCreate,
    TestRunResultUpdate,
)

if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing import Dict as TypedDict


try:
    # Change here if project is renamed and does not equal the package name
    dist_name = "qase-robotframework"
    __version__ = get_distribution(dist_name).version
except DistributionNotFound:
    __version__ = "unknown"
finally:
    del get_distribution, DistributionNotFound


logger = logging.getLogger("qase-robotframework")

STATUSES = {
    "PASS": TestRunResultStatus.PASSED,
    "FAIL": TestRunResultStatus.FAILED,
}


class Envs(Enum):
    TOKEN = "QASE_API_TOKEN"
    PROJECT = "QASE_PROJECT"
    RUN_ID = "QASE_RUN_ID"
    RUN_NAME = "QASE_RUN_NAME"
    DEBUG = "QASE_DEBUG"


class StartSuiteModel(TypedDict):
    id: str
    longname: str
    doc: str
    metadata: dict
    source: str
    suites: List[str]
    tests: List[str]
    totaltests: int
    starttime: str


class EndSuiteModel(TypedDict):
    id: str
    longname: str
    doc: str
    metadata: dict
    source: str
    starttime: str
    endtime: str
    elapsedtime: int
    status: str
    statistics: str
    message: str


class StartTestModel(TypedDict):
    id: str
    longname: str
    originalname: str
    doc: dict
    tags: List[str]
    critical: str
    template: str
    lineno: int
    starttime: str


class EndTestModel(TypedDict):
    id: str
    longname: str
    originalname: str
    doc: dict
    tags: List[str]
    critical: str
    template: str
    lineno: int
    starttime: str
    endtime: str
    elapsedtime: int
    status: str
    message: str


class StartKeywordModel(TypedDict):
    type: str
    kwname: str
    libname: str
    doc: dict
    args: List[str]
    assign: List[str]
    tags: List[str]
    starttime: str


class EndKeywordModel(TypedDict):
    type: str
    kwname: str
    libname: str
    doc: dict
    args: List[str]
    assign: List[str]
    tags: List[str]
    starttime: str
    endtime: str
    elapsedtime: int
    status: str


class MissingStepIdentifierException(Exception):
    pass


class Listener:
    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read("tox.ini")

        self.token = self.get_param(Envs.TOKEN)
        self.project_code = self.get_param(Envs.PROJECT)
        if not self.token or not self.project_code:
            raise ValueError("Token and Project code should be provided")
        self.api = client.QaseApi(self.token)
        self.run_id = self.get_param(Envs.RUN_ID)
        self.run_name = self.get_param(Envs.RUN_NAME)
        self.results = {}
        self.history = []
        self.debug = bool(self.get_param(Envs.DEBUG))
        if self.debug:
            logger.setLevel(logging.DEBUG)
            ch = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            ch.setFormatter(formatter)
            logger.addHandler(ch)

    def get_param(self, param: Envs):
        param: str = param.value
        return os.environ.get(
            param, self.config.get("qase", param.lower(), fallback=None)
        )

    def start_suite(self, name, attributes: StartSuiteModel):
        logger.debug("Starting suite '%s'", name)
        if not self.run_id and attributes.get("totaltests") > 0:
            name = self.run_name or "Automated Run {}".format(
                str(datetime.now())
            )
            logger.info("Creating new run with name: %s", name)
            res = self.api.runs.create(
                self.project_code, TestRunCreate(name, [])
            )
            self.run_id = res.id
        elif self.run_id:
            logger.info("Using run %s to publish test results", self.run_id)

    def start_test(self, name, attributes: StartTestModel):
        logger.debug("Starting test '%s'", name)
        ids = self._extract_ids(attributes.get("tags"))
        if len(ids) == 1:
            case_info = self.api.cases.get(self.project_code, ids[0])
        else:
            case_info = None
        data = {
            "hashes": [],
            "case_info": case_info,
            "use_steps": bool(case_info and case_info.steps),
            "steps_count": 0,
            "steps": [],
        }
        for _id in ids:
            logger.info("Adding result to case %s-%s", self.project_code, _id)
            req_data = TestRunResultCreate(
                _id, TestRunResultStatus.IN_PROGRESS
            )
            res = self.api.results.create(
                self.project_code, self.run_id, req_data
            )
            data.get("hashes").append(res.hash)
        self.results[attributes.get("id")] = data
        self.history.append(data)

    def end_test(self, name, attributes: EndTestModel):
        logger.debug("Finishing test '%s'", name)
        for hash in self.results.get(attributes.get("id"), {}).get(
            "hashes", []
        ):
            logger.info(
                "Finished case result with hash: %s, %s, error: %s",
                hash,
                attributes.get("status"),
                attributes.get("message"),
            )
            req_data = TestRunResultUpdate(
                STATUSES[attributes.get("status")],
                time=attributes.get("elapsedtime"),
                stacktrace=attributes.get("message"),
                steps=self.results.get(attributes.get("id"), {}).get(
                    "steps", []
                ),
            )
            self.api.results.update(
                self.project_code, self.run_id, hash, req_data
            )

    def end_keyword(self, name, attributes: EndKeywordModel):
        logger.debug("Finishing step '%s'", name)
        last_item = self.history[-1]
        case = last_item.get("case_info")
        if last_item.get("use_steps"):
            position = self._get_step_position(
                attributes["kwname"], case, last_item.get("steps_count")
            )
            if position:
                data = TestRunResultStepCreate(
                    position,
                    STATUSES[attributes["status"]],
                    comment=f"Step `{name}` with args: {attributes['args']}",
                )
                last_item["steps"].append(data)
            else:
                logger.info(
                    "Can't find suitable step in %s-%s for step '%s'",
                    self.project_code,
                    case.id,
                    name,
                )
            last_item["steps_count"] += 1
        elif case:
            logger.info(
                "Case %s-%s does not have steps, "
                "skipping step result publishing",
                self.project_code,
                case.id,
            )

    def log_message(self, message):
        logger.debug("Log:", message)

    def _extract_ids(self, list_of_tags: List[str]) -> List[int]:
        return [
            int(re.match(r"Q-(\d+)", tag).groups()[0])
            for tag in list_of_tags
            if re.fullmatch(r"Q-\d+", tag)
        ]

    def _get_step_position(
        self, step_name: str, case: TestCaseInfo, previous_step: int
    ) -> Optional[int]:
        for pos, step in enumerate(case.steps):
            if re.match(
                r"{}.*".format(step_name.lower()), step.get("action").lower()
            ):
                if pos >= previous_step:
                    return pos + 1
        logger.warning(
            MissingStepIdentifierException(
                "Missing step for name {}".format(step_name)
            )
        )
        return None
