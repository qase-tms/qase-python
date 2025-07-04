import threading
import urllib.parse

from datetime import datetime
from typing import List, Union
from .. import Logger, ReporterException
from ..client.api_v2_client import ApiV2Client
from ..client.base_api_client import BaseApiClient
from ..models import Result
from ..models.config.qaseconfig import QaseConfig

DEFAULT_BATCH_SIZE = 200
DEFAULT_THREAD_COUNT = 4


class QaseTestOps:

    def __init__(self, config: QaseConfig, logger: Logger) -> None:
        self.config = config
        self.logger = logger
        self.__baseUrl = self.__get_host(config.testops.api.host)

        self.client = self._prepare_client()

        run_id = self.config.testops.run.id
        plan_id = self.config.testops.plan.id

        self.project_code = self.config.testops.project
        self.run_id = int(run_id) if run_id else run_id
        self.plan_id = int(plan_id) if plan_id else plan_id
        self.defect = self.config.testops.defect
        self.complete_after_run = self.config.testops.run.complete
        self.environment = None

        self.batch_size = min(2000, max(1, int(self.config.testops.batch.size or DEFAULT_BATCH_SIZE)))
        self.send_semaphore = threading.Semaphore(DEFAULT_THREAD_COUNT)  # Semaphore to limit concurrent sends
        self.lock = threading.Lock()
        self.count_running_threads = 0

        environment = self.config.environment
        if environment:
            if isinstance(environment, int) or (isinstance(environment, str) and environment.isnumeric()):
                self.environment = environment
            elif isinstance(environment, str):
                self.environment = self.client.get_environment(environment, self.project_code)

        run_title = self.config.testops.run.title
        if run_title and run_title != '':
            self.run_title = run_title
        else:
            self.run_title = "Automated Run {}".format(str(datetime.now()))

        run_description = self.config.testops.run.description
        if run_description and run_description != '':
            self.run_description = run_description
        else:
            self.run_description = "Automated Run {}".format(str(datetime.now()))

        self.run = None

        # Container for test results
        self.results = []

        # Container for processed results
        self.processed = []
        self.attachments = {}

        """Verify that project exists in TestOps"""
        self.client.get_project(self.project_code)

    def _prepare_client(self) -> BaseApiClient:
        return ApiV2Client(self.config, self.logger)

    def _send_results_threaded(self, results):
        try:
            self.client.send_results(self.project_code, self.run_id, results)
            with self.lock:
                self.processed.extend(results)
        except Exception as e:
            with self.lock:
                self.logger.log(f"Error at sending results for run {self.run_id}: {e}", "error")
            raise  # Re-raise the exception to be caught by the thread handler
        finally:
            self.count_running_threads -= 1
            self.send_semaphore.release()  # Release semaphore whether success or exception

    def _send_results(self) -> None:
        if self.results:
            # Acquire semaphore before starting the send operation
            self.send_semaphore.acquire()
            self.count_running_threads += 1
            results_to_send = self.results.copy()
            self.results = []

            # Start a new thread for sending results
            send_thread = threading.Thread(target=self._send_results_threaded, args=(results_to_send,))
            send_thread.start()
        else:
            self.logger.log("No results to send", "info")

    def set_run_id(self, run_id) -> None:
        self.run_id = int(run_id)

    # Lifecycle methods
    def start_run(self) -> str:
        if self.plan_id and not self.run_id:
            self.run_id = self.client.create_test_run(project_code=self.project_code, title=self.run_title,
                                                      description=self.run_description, plan_id=self.plan_id,
                                                      environment_id=self.environment)
        if not self.run_id and not self.plan_id:
            self.run_id = self.client.create_test_run(project_code=self.project_code, title=self.run_title,
                                                      description=self.run_description, environment_id=self.environment)
        if self.run_id and not self.client.check_test_run(self.project_code, self.run_id):
            raise ReporterException("Unable to find given test run.")
        return self.run_id

    def complete_run(self) -> None:
        if len(self.results) > 0:
            self._send_results()

        while self.count_running_threads > 0:
                pass    
        
        if self.complete_after_run:
            self.logger.log_debug("Completing run")
            self.client.complete_run(self.project_code, self.run_id)
            self.logger.log_debug("Run completed")

    def complete_worker(self) -> None:
        if len(self.results) > 0:
            self._send_results()
        while self.count_running_threads > 0:
            pass
        self.logger.log_debug("Worker completed")

    def add_result(self, result: Result) -> None:
        if result.get_status() == 'failed':
            self.__show_link(result.testops_ids, result.title)
        self.results.append(result)
        if len(self.results) >= self.batch_size:
            self._send_results()

    def get_results(self) -> List:
        return self.results + self.processed

    def set_results(self, results) -> None:
        self.results = results

    def __show_link(self, ids: Union[None, List[int]], title: str):
        link = self.__prepare_link(ids, title)
        self.logger.log(f"See why this test failed: {link}", "info")

    def __prepare_link(self, ids: Union[None, List[int]], title: str):
        link = f"{self.__baseUrl}/run/{self.project_code}/dashboard/{self.run_id}?source=logs&status=%5B2%5D&search="
        if ids is not None and len(ids) > 0:
            return f"{link}{self.project_code}-{ids[0]}"
        return f"{link}{urllib.parse.quote_plus(title)}"

    @staticmethod
    def __get_host(host: str):
        if host == 'qase.io':
            return 'https://app.qase.io'

        return f'https://{host.replace("api", "app")}'
