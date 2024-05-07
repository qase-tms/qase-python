import threading

from datetime import datetime
from typing import List
from .. import ConfigManager, Logger, ReporterException
from ..client.api_v1_client import ApiV1Client
from ..client.base_api_client import BaseApiClient
from ..models import Result

DEFAULT_BATCH_SIZE = 200


class QaseTestOps:

    def __init__(self, config: ConfigManager, logger: Logger) -> None:
        self.config = config
        self.logger = logger

        self.client = self._prepare_client()

        run_id = self.config.get('testops.run.id')
        plan_id = self.config.get('testops.plan.id')

        self.project_code = self.config.get('testops.project')
        self.run_id = int(run_id) if run_id else run_id
        self.plan_id = int(plan_id) if plan_id else plan_id
        self.defect = self.config.get('testops.defect', False, bool)
        self.complete_after_run = self.config.get('testops.run.complete', True, bool)
        self.environment = None

        self.batch_size = min(2000, max(1, int(self.config.get('testops.batch.size', DEFAULT_BATCH_SIZE))))
        self.send_semaphore = threading.Semaphore(
            self.config.get('testops.batch.threads', 4))  # Semaphore to limit concurrent sends
        self.lock = threading.Lock()

        environment = self.config.get('environment', None)
        if environment:
            if isinstance(environment, int) or (isinstance(environment, str) and environment.isnumeric()):
                self.environment = environment
            elif isinstance(environment, str):
                self.environment = self.client.get_environment(environment, self.project_code)

        run_title = self.config.get('testops.run.title', None)
        if run_title and run_title != '':
            self.run_title = run_title
        else:
            self.run_title = "Automated Run {}".format(str(datetime.now()))

        run_description = self.config.get('testops.run.description', None)
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
        if self.config.get('testops.usev2', False, bool):
            from ..client.api_v2_client import ApiV2Client
            return ApiV2Client(self.config, self.logger)
        return ApiV1Client(self.config, self.logger)

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
            self.send_semaphore.release()  # Release semaphore whether success or exception

    def _send_results(self) -> None:
        if self.results:
            # Acquire semaphore before starting the send operation
            self.send_semaphore.acquire()
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
        if self.complete_after_run:
            self.client.complete_run(self.project_code, self.run_id)

    def complete_worker(self) -> None:
        if len(self.results) > 0:
            self._send_results()

    def add_result(self, result: Result) -> None:
        self.results.append(result)
        if len(self.results) >= self.batch_size:
            self._send_results()

    def get_results(self) -> List:
        return self.results + self.processed

    def set_results(self, results) -> None:
        self.results = results
