import configparser
import logging
import os
import re
import sys
from datetime import datetime
from enum import Enum
from pkg_resources import DistributionNotFound, get_distribution
from typing import List

from qaseio import client
from qaseio.client.models import (
    TestRunCreate,
    TestRunResultCreate,
    TestRunResultStatus,
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

    def get_param(self, param: Envs):
        param: str = param.value
        return os.environ.get(
            param, self.config.get("qase", param.lower(), fallback=None)
        )

    def start_suite(self, name, attributes: StartSuiteModel):
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
        ids = self._extract_ids(attributes.get("tags"))
        data = {"hashes": []}
        for _id in ids:
            logger.info("Running test %s-%s", self.project_code, _id)
            req_data = TestRunResultCreate(
                _id, TestRunResultStatus.IN_PROGRESS
            )
            res = self.api.results.create(
                self.project_code, self.run_id, req_data
            )
            data.get("hashes").append(res.hash)
        self.results[attributes.get("id")] = data

    def end_test(self, name, attributes: EndTestModel):
        for hash in self.results.get(attributes.get("id"), {}).get(
            "hashes", []
        ):
            req_data = TestRunResultUpdate(
                STATUSES[attributes.get("status")],
                time=attributes.get("elapsedtime"),
                stacktrace=attributes.get("message"),
            )
            self.api.results.update(
                self.project_code, self.run_id, hash, req_data
            )

    def log_message(self, message):
        logger.debug("Log:", message)

    def _extract_ids(self, list_of_tags: List[str]) -> List[int]:
        return [
            int(re.match(r"Q-(\d+)", tag).groups()[0])
            for tag in list_of_tags
            if re.fullmatch(r"Q-\d+", tag)
        ]
