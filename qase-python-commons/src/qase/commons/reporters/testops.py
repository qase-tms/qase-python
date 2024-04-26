import threading
import certifi

from qaseio.api.attachments_api import AttachmentsApi
from qaseio.api.environments_api import EnvironmentsApi
from qaseio.api.projects_api import ProjectsApi
from qaseio.api.results_api import ResultsApi
from qaseio.api.runs_api import RunsApi
from qaseio.api_client import ApiClient
from qaseio.configuration import Configuration
from qaseio.models import RunCreate, ResultcreateBulk
from datetime import datetime
from typing import List, Dict, Union
from .. import ConfigManager, Logger, ReporterException
from ..models import Attachment, Step, Result
from ..models.step import StepType

DEFAULT_BATCH_SIZE = 200


class QaseTestOps:

    def __init__(self, config: ConfigManager, logger: Logger) -> None:
        self.config = config
        self.logger = logger

        self._prepare_client()

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
                self.environment = self._get_environment(environment, self.project_code)

        run_title = self.config.get('testops.run.title', None)
        if run_title and run_title != '':
            self.run_title = run_title
        else:
            self.run_title = "Automated Run {}".format(str(datetime.now()))

        self.run = None

        # Container for test results
        self.results = []

        # Container for processed results
        self.processed = []
        self.attachments = {}

        """Verify that project exists in TestOps"""
        self._get_project(self.project_code)

    def _prepare_client(self) -> None:
        try:
            self.logger.log_debug("Preparing API client")
            configuration = Configuration()
            configuration.api_key['TokenAuth'] = self.config.get('testops.api.token')
            configuration.ssl_ca_cert = certifi.where()
            host = self.config.get('testops.api.host', 'qase.io')
            if self.config.get('testops.api.enterprise', False, bool):
                configuration.host = f'https://api-{host}/v1'
                self.web = f'https://{host}'
            else:
                configuration.host = f'https://api.{host}/v1'
                self.web = f'https://app.{host}'

            self.client = ApiClient(configuration)
            self.logger.log_debug("API client prepared")
        except Exception as e:
            self.logger.log(f"Error at preparing API client: {e}", "error")
            raise ReporterException(e)

    # Method loads project from Qase TestOps by code and returns project data
    def _get_project(self, code: str) -> Dict:
        try:
            self.logger.log_debug(f"Getting project {code}")
            response = ProjectsApi(self.client).get_project(code=code)
            if hasattr(response, 'result'):
                self.logger.log_debug(f"Project {code} found: {response.result.to_json()}")
                return response.result
            raise ReporterException("Unable to find given project code")
        except Exception as e:
            self.logger.log("Exception when calling ProjectApi->get_project: %s\n" % e, "error")
            raise ReporterException("Exception when calling ProjectApi")

    # Method loads environment by name and returns environment id
    # If environment not found or exception raised, returns None
    def _get_environment(self, environment: str, code: str) -> Union[str, None]:
        try:
            self.logger.log_debug(f"Getting environment {environment}")
            api_instance = EnvironmentsApi(self.client)
            response = api_instance.get_environments(code=code)
            if hasattr(response, 'result') and hasattr(response.result, 'entities'):
                for env in response.result.entities:
                    if env.slug == environment:
                        self.logger.log_debug(f"Environment {environment} found: {env.to_json()}")
                        return env.id
            self.logger.log_debug(f"Environment {environment} not found")
            return None
        except Exception as e:
            self.logger.log("Exception when calling EnvironmentsApi->get_environments: %s\n" % e, "error")
            raise ReporterException(e)

    def _send_results_threaded(self, results):
        try:
            api_results = ResultsApi(self.client)
            results_to_send = [self._prepare_result(result) for result in results]
            self.logger.log_debug(f"Sending results for run {self.run_id}: {results_to_send}")
            api_results.create_result_bulk(
                code=self.project_code,
                id=self.run_id,
                resultcreate_bulk=ResultcreateBulk(
                    results=results_to_send
                )
            )
            self.logger.log_debug(f"Results for run {self.run_id} sent successfully")
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

    def _old_send_results(self) -> None:
        if self.results and len(self.results) > 0:
            results = []
            for result in self.results:
                results.append(self._prepare_result(result))

            api_results = ResultsApi(self.client)
            try:
                api_results.create_result_bulk(
                    code=self.project_code,
                    id=self.run_id,
                    resultcreate_bulk=ResultcreateBulk(
                        results=results
                    )
                )
            except Exception as e:
                self.logger.log(f"Error at sending results for run {self.run_id}: {e}", "error")
                raise ReporterException(e)

            # Moving processed results to another list, so we can use them later for fallback.
            self.processed += self.results
            self.results = []
        else:
            self.logger.log("No results to send", "info")

    def _prepare_result(self, result: Result) -> Dict:
        attached = []
        if result.attachments:
            for attachment in result.attachments:
                attached.extend(self._upload(attachment))

        steps = []
        for step in result.steps:
            prepared = self._prepare_step(step)
            steps.append(prepared)

        case_data = {
            "title": result.get_title(),
            "description": result.get_field('description'),
            "preconditions": result.get_field('preconditions'),
            "postconditions": result.get_field('postconditions'),
        }

        for key, param in result.params.items():
            # Hack to match old TestOps API
            if param == "": result.params[key] = "empty"

        if result.get_field('severity'):
            case_data["severity"] = result.get_field('severity')

        if result.get_field('priority'):
            case_data["priority"] = result.get_field('priority')

        if result.get_field('layer'):
            case_data["layer"] = result.get_field('layer')

        if result.get_suite_title():
            case_data["suite_title"] = "\t".join(result.get_suite_title().split("."))

        result_model = {
            "status": result.execution.status,
            "stacktrace": result.execution.stacktrace,
            "time_ms": result.execution.duration,
            "comment": result.message,
            "attachments": [attach.hash for attach in attached],
            "steps": steps,
            "param": result.params,
            "defect": self.defect
        }

        test_ops_id = result.get_testops_id()

        if test_ops_id:
            result_model["case_id"] = test_ops_id
            result_model["case"] = None
            return result_model

        result_model["case_id"] = None
        result_model["case"] = case_data

        self.logger.log_debug(f"Prepared result: {result_model}")

        return result_model

    def _complete_run(self) -> None:
        api_runs = RunsApi(self.client)
        self.logger.log(f"Completing run {self.run_id}", "info")
        res = api_runs.get_run(self.project_code, self.run_id).result
        if res.status == 1:
            self.logger.log(f"Run {self.run_id} already completed", "info")
            return
        try:
            api_runs.complete_run(self.project_code, self.run_id)
            self.logger.log(f"Run {self.run_id} was completed successfully", "info")
        except Exception as e:
            self.logger.log(f"Error at completing run {self.run_id}: {e}", "error")
            raise ReporterException(e)

    def set_run_id(self, run_id) -> None:
        self.run_id = int(run_id)

    def _load_run(self) -> bool:
        api_runs = RunsApi(self.client)
        if self.run_id and isinstance(self.run_id, int):
            run = api_runs.get_run(
                code=self.project_code,
                id=self.run_id,
            ).result
            if run.id:
                return True
        return False

    def _create_run(self, plan_id=None, environment_id=None, cases: List = []) -> None:
        # TODO: read description from configs
        kwargs = dict(
            title=self.run_title,
            cases=cases,
            environment_id=(int(environment_id) if environment_id else None),
            plan_id=(int(plan_id) if plan_id else plan_id),
            is_autotest=True
        )
        self.logger.log_debug(f"Creating test run with parameters: {kwargs}")
        try:
            result = RunsApi(self.client).create_run(
                code=self.project_code,
                run_create=RunCreate(**{k: v for k, v in kwargs.items() if v is not None})
            )
            self.run_id = result.result.id
            self.run = result.result

            self.logger.log(f"Test run was created: {self.web}/run/{self.project_code}/dashboard/{self.run_id}", "info")

        except Exception as e:
            self.logger.log(f"Error at creating test run: {e}", "error")
            raise ReporterException(e)

    def _upload(self, attachment: Attachment) -> Dict:
        try:
            return AttachmentsApi(self.client).upload_attachment(
                self.project_code, file=[attachment.get_for_upload()],
            ).result
        except Exception as e:
            self.logger.log(f"Error at uploading attachment: {e}", "error")
            raise ReporterException(e)

    # This method contains a lot of hacks to match old TestOps API.
    def _prepare_step(self, step: Step) -> Dict:
        prepared_children = []

        try:
            prepared_step = {"time": step.execution.duration, "status": step.execution.status}

            if step.execution.status == 'untested':
                prepared_step["status"] = 'passed'

            if step.step_type == StepType.TEXT:
                prepared_step['action'] = step.data.action
                if step.data.expected_result:
                    prepared_step['expected_result'] = step.data.expected_result

            if step.step_type == StepType.REQUEST:
                prepared_step['action'] = step.data.request_method + " " + step.data.request_url
                if step.data.request_body:
                    step.attachments.append(
                        Attachment(file_name='request_body.txt', content=step.data.request_body, mime_type='text/plain',
                                   temporary=True))
                if step.data.request_headers:
                    step.attachments.append(
                        Attachment(file_name='request_headers.txt', content=step.data.request_headers,
                                   mime_type='text/plain', temporary=True))
                if step.data.response_body:
                    step.attachments.append(Attachment(file_name='response_body.txt', content=step.data.response_body,
                                                       mime_type='text/plain', temporary=True))
                if step.data.response_headers:
                    step.attachments.append(
                        Attachment(file_name='response_headers.txt', content=step.data.response_headers,
                                   mime_type='text/plain', temporary=True))

            if step.step_type == StepType.GHERKIN:
                prepared_step['action'] = step.data.keyword

            if step.step_type == StepType.SLEEP:
                prepared_step['action'] = f"Sleep for {step.data.duration} seconds"

            if step.attachments:
                uploaded_attachments = []
                for file in step.attachments:
                    uploaded_attachments.extend(self._upload(file))
                prepared_step['attachments'] = [attach.hash for attach in uploaded_attachments]

            if step.steps:
                for substep in step.steps:
                    prepared_children.append(self._prepare_step(substep))
                prepared_step["steps"] = prepared_children
            return prepared_step
        except Exception as e:
            self.logger.log(f"Error at preparing step: {e}", "error")
            raise ReporterException(e)

    # Lifecycle methods
    def start_run(self) -> str:
        if self.plan_id and not self.run_id:
            self._create_run(plan_id=self.plan_id, environment_id=self.environment)
        if not self.run_id and not self.plan_id:
            self._create_run(environment_id=self.environment)
        if not self.run and not self._load_run:
            raise ReporterException("Unable to find given test run.")
        return self.run_id

    def complete_run(self, exit_code=None) -> None:
        if len(self.results) > 0:
            self._send_results()
        if self.complete_after_run:
            self._complete_run()

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
