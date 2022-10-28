import configparser
import logging
import glob
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
    "SKIP": TestRunResultStatus.SKIPPED,
}


class Envs(Enum):
    TOKEN = "QASE_API_TOKEN"
    PROJECT = "QASE_PROJECT"
    RUN_ID = "QASE_RUN_ID"
    RUN_NAME = "QASE_RUN_NAME"
    DEBUG = "QASE_DEBUG"
    RUN_COMPLETE = "QASE_RUN_COMPLETE"
    STEPS_RESULTS = "QASE_STEPS_RESULTS"
    SCREENSHOT_PATH = "QASE_SCREENSHOT_PATH"


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
        self.debug = self.get_param(Envs.DEBUG).lower() in ['true', '1']
        self.complete_run = self.get_param(Envs.RUN_COMPLETE).lower() in ['true', '1']
        self.steps_results = self.get_param(Envs.STEPS_RESULTS).lower() in ['true', '1']
        self.screenshot_path = self.get_param(Envs.SCREENSHOT_PATH)
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
        if self.results.get(attributes.get("id")):
            for hash in self.results.get(attributes.get("id"), {}).get(
                "hashes", []
            ):
                logger.info(
                    "Finished case result with hash: %s, %s, error: %s",
                    hash,
                    attributes.get("status"),
                    attributes.get("message"),
                )

                # Only upload screenshot if testcase is failed
                if attributes.get("status").lower() == "fail":
                    attachment_hashes = self._upload_attachments_and_get_hashes(self._get_screenshots(self.screenshot_path))
                else:
                    attachment_hashes = []

                req_data = TestRunResultUpdate(
                    STATUSES[attributes.get("status")],
                    time_ms=attributes.get("elapsedtime"),
                    stacktrace=attributes.get("message"),
                    steps=self.results.get(attributes.get("id"), {}).get(
                        "steps", []
                    ),
                    attachments=attachment_hashes
                )
                self.api.results.update(
                    self.project_code, self.run_id, hash, req_data
                )
            self.history.remove(self.results.get(attributes.get("id")))

    def end_keyword(self, name, attributes: EndKeywordModel):
        if self.history:
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
                        comment=f"Step `{name}` with args: {attributes['args']}",  # noqa: E501
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
        else:
            logger.debug("Skipping keyword '%s'", name)

    def end_suite(self, name, attributes: EndSuiteModel):
        logger.debug("Finishing suite '%s'", name)
        if not self.history:
            logger.info("Finishing run with name: %s", name)
            if self.complete_run:
                self.complete()

    def complete(self):
        logger.info("complete run executing")
        if self.run_id and self.complete_run:
            print()
            print(f"Finishing run {self.run_id}")
            res = self.api.runs.get(self.project_code, self.run_id)
            if res.status == 1:
                print(f"Run {self.run_id} already finished")
                return
            try:
                self.api.runs.complete(self.project_code, self.run_id)
                print(f"Run {self.run_id} was finished successfully")
            except Exception as e:
                print(f"Run {self.run_id} was finished with error: {e}")

    def log_message(self, message):
        logger.debug("Log:", message)

    def _extract_ids(self, list_of_tags: List[str]) -> List[int]:
        id = re.compile(r"Q-(\d+)", re.IGNORECASE)
        return [
            int(id.match(tag).groups()[0]) for tag in list_of_tags if id.fullmatch(tag)
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

    def _upload_attachments_and_get_hashes(self, list_of_files):
        hash_list = []
        for eachFile in list_of_files:
            attach_res = self.api.attachments.upload(self.project_code, eachFile)
            hash_list.append(attach_res[0].hash)

        return hash_list

    # Since RobotFramework does not spit the screenshot filename or filepath when testcase are failed.
    # Prerequisite for this functionality to work is to have a screenshot folder, setup when calling SeleniumLibrary
    # from RobotFramework so as to pick the latest file assuming a screenshot was saved when testcase failed
    def _get_screenshots(self, screenshotFolderPath):
        files_path = os.path.join(screenshotFolderPath, '*')
        files = sorted(glob.iglob(files_path), key=os.path.getctime, reverse=True)
        return [files[0]]