import configparser
import logging
import os
import re
import uuid
import time
from datetime import datetime
from pkg_resources import DistributionNotFound, get_distribution
from typing import List


from qaseio.commons import QaseTestOps
from qaseio.commons import QaseUtils
from qaseio.commons import QaseReport
from .types import Envs, STATUSES
from .models import * 

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = "qase-robotframework"
    __version__ = get_distribution(dist_name).version
except DistributionNotFound:
    __version__ = "unknown"
finally:
    del get_distribution, DistributionNotFound

logger = logging.getLogger("qase-robotframework")

class QaseListener:
    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read("tox.ini")

        if (self._get_param(Envs.MODE) and self._get_param(Envs.MODE).lower() == 'testops'):
            token = self._get_param(Envs.TESTOPS_API_TOKEN)
            project_code = self._get_param(Envs.TESTOPS_PROJECT)

            if not token or not project_code:
                raise ValueError("Token and Project code should be provided")
            
            run_title = "Automated Run {}".format(str(datetime.now()))
            if (self._get_param(Envs.TESTOPS_RUN_TITLE, None)):
                run_title = self._get_param(Envs.TESTOPS_RUN_TITLE, None)
            
            self.reporter = QaseTestOps(
                api_token=token,
                project_code=project_code,
                run_id=self._get_param(Envs.TESTOPS_RUN_ID, None),
                plan_id=self._get_param(Envs.TESTOPS_PLAN_ID, None),
                complete_run=self._get_param(Envs.TESTOPS_COMPLETE_RUN) and self._get_param(Envs.TESTOPS_COMPLETE_RUN).lower() in ['true', '1'],
                mode=self._get_param(Envs.TESTOPS_MODE, 'async'),
                run_title=run_title,
                host=self._get_param(Envs.TESTOPS_HOST, 'qase.io'),
                environment=self._get_param(Envs.ENVIRONMENT, None)
            )
        else:
            self.reporter = QaseReport(
                report_path=self._get_param(Envs.REPORT_PATH, 'build/qase-report'),
            )

        self.result = {}
        self.steps = {}
        self.step_uuid = None
        self.suite = {}

        self.debug = self._get_param(Envs.DEBUG) and self._get_param(Envs.DEBUG).lower() in ['true', '1']
        if self.debug:
            logger.setLevel(logging.DEBUG)
            ch = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            ch.setFormatter(formatter)
            logger.addHandler(ch)

        self.reporter.start_run()

    def _get_param(self, param: Envs, default=None):
        param: str = param.value
        return os.environ.get(
            param, self.config.get("qase", param.lower(), fallback=default)
        )

    def start_suite(self, name, attributes):
        self.suite = {
            "title": name,
            "description": attributes["doc"]
        }
        logger.debug("Starting suite '%s'", name)

    def start_test(self, name, attributes: StartTestModel):
        logger.debug("Starting test '%s'", name)
        
        self.result = {
            'is_api_result': True,
            'case': {},
            'steps': {},
            'param': {},
        }
        self.result['uuid'] = str(uuid.uuid4())
        self.result["started_at"] = time.time()
        
        case_id = self._extract_ids(attributes.get("tags"))
        if (case_id):
            self.result["case_id"] = int(case_id)

    def end_test(self, name, attributes: EndTestModel):
        logger.debug("Finishing test '%s'", name)

        completed_at = time.time()
        self.result['time_ms'] = int((completed_at - self.result.get("started_at")) * 1000)
        self.result['completed_at'] = completed_at
        self.result['status'] = STATUSES[attributes.get("status")]
        self.result['stacktrace'] = attributes.get("message")
        self.result['case'] = {}
        self.result['case']['title'] = name
        self.result['case']['description'] = attributes.get("doc")
        if (self.suite):
            self.result['case']['suite_title'] = self.suite.get('title', None)
            #self.result['case']['suite_description'] = self.suite.get('description', None) // Not support in Qase API yet

        self.reporter.add_result(self.result, QaseUtils().build_tree(self.steps))

        self.result = {}
        self.steps = {}
        self.step_uuid = None

        logger.info(
            "Finished case result: %s, error: %s",
            attributes.get("status"),
            attributes.get("message"),
        )

    def start_keyword(self, name, attributes):
        id = str(uuid.uuid4())

        self.steps[id] = {
            "uuid": id,
            "started_at": time.time(),
            "attachments": [],
            "steps": {},
            "parent_id": self.step_uuid
        }

        self.step_uuid = id

    def end_keyword(self, name, attributes):
        now = time.time()

        self.steps[self.step_uuid]['status'] = STATUSES[attributes["status"]]
        self.steps[self.step_uuid]['action'] = attributes["kwname"]
        self.steps[self.step_uuid]['duration'] = int((now - self.steps[self.step_uuid]['started_at'])*1000)
        self.steps[self.step_uuid]['completed_at'] = now
        self.steps[self.step_uuid]['comment'] = f"Step `{name}` with args: {attributes['args']}"

        self.step_uuid = self.steps[self.step_uuid]['parent_id']

    def end_suite(self, name, attributes: EndSuiteModel):
        self.suite = {}
        logger.debug("Finishing suite '%s'", name)

    def close(self):
        logger.info("complete run executing")
        self.reporter.complete_run(True)

    def log_message(self, message):
        logger.debug("Log:", message)

    def _extract_ids(self, list_of_tags: List[str]):
        id = re.compile(r"Q-(\d+)", re.IGNORECASE)
        for tag in list_of_tags:
            if id.fullmatch(tag):
                return int(id.match(tag).groups()[0])
        return None