from qaseio.api_client import ApiClient
from qaseio.configuration import Configuration
from qaseio.api.attachments_api import AttachmentsApi
from qaseio.api.environments_api import EnvironmentsApi
from qaseio.api.projects_api import ProjectsApi
from qaseio.api.results_api import ResultsApi
from qaseio.api.runs_api import RunsApi
from qaseio.models import RunCreate, ResultcreateBulk
from qaseio.rest import ApiException

from qase.commons.models import Attachment, Step, Result

from qase.commons import ConfigManager, Logger, ReporterException
from datetime import datetime

from typing import List, Dict, Union

import more_itertools, certifi

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
        self.defect = self.config.get('testops_defect', False, bool)
        self.complete_after_run = self.config.get('testops.run.complete', False, bool)
        self.environment = None
        
        self.chunk_size = min(2000, max(10, int(self.config.get('testops.chunk', 200))))
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
        except Exception as e:
            self.logger.log(f"Error at preparing API client: {e}", "error")
            raise ReporterException(e)

    # Method loads project from Qase TestOps by code and returns project data
    def _get_project(self, code: str) -> Dict:
        try:
            response = ProjectsApi(self.client).get_project(code = code)
            if hasattr(response, 'result'):
                return response.result
            raise ReporterException("Unable to find given project code")
        except Exception as e:
            self.logger.log("Exception when calling ProjectApi->get_project: %s\n" % e, "error")
            raise ReporterException("Exception when calling ProjectApi")

    # Method loads environment by name and returns environment id
    # If environment not found or exception raised, returns None
    def _get_environment(self, environment: str, code: str) -> Union[str, None]:
        try:
            api_instance = EnvironmentsApi(self.client)
            response = api_instance.get_environments(code = code)
            if hasattr(response, 'result') and hasattr(response.result, 'entities'):
                for env in response.result.entities:
                    if env.slug == environment:
                        return env.id
            return None
        except Exception as e:
            self.logger.log("Exception when calling EnvironmentsApi->get_environments: %s\n" % e, "error")
            raise ReporterException(e)

    def _send_results(self) -> None:
        if self.results and len(self.results) > 0:
            results = []
            for result in self.results:
                results.append(self._prepare_result(result))

            api_results = ResultsApi(self.client)
            self.logger.log(f"Sending results to test run {self.run_id}. Total: {len(results)}.", "info")

            i = 1

            for chunk in more_itertools.chunked(results, self.chunk_size):
                try:
                    self.logger.log(f"Sending chunk #{i}. Chunk size: {len(chunk)}...", "info")
                    api_results.create_result_bulk(
                        code=self.project_code,
                        id=self.run_id,
                        resultcreate_bulk=ResultcreateBulk(
                            results=chunk
                        )
                    )
                    self.logger.log(f"Chunk #{i} was sent successfully.", "info")
                    i = i+1
                except Exception as e:
                    self.logger.log(f"Error at sending results for run {self.run_id} (Chunk #{i}): {e}", "error")
                    raise ReporterException(e)
                
            # Moving processed results to another list, so we can use them later for fallback.
            self.processed = self.results
            self.results = []
        else:
            self.logger.log("No results to send", "info")

    def _prepare_result(self, result: Dict) -> Dict:
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
            "precondtions": result.get_field('precondtions'),
            "postconditions": result.get_field('postconditions'),
        }

        for key, param in result.params.items():
            # Hack to match old TestOps API
            if param == "": result.params[key] = "empty"

        if (result.get_field('severity')):
            case_data["severity"] = result.get_field('severity')

        if (result.get_field('priority')):
            case_data["priority"] = result.get_field('priority')

        if (result.get_field('layer')):
            case_data["layer"] = result.get_field('layer')

        if result.get_suite_title():
            case_data["suite_title"] = "\t".join(result.get_suite_title().split("."))

        return {
            "case_id": result.get_testops_id(),
            "status": result.execution.status,
            "stacktrace": result.execution.stacktrace,
            "time_ms": result.execution.duration,
            "comment": result.message,
            "attachments": [attach.hash for attach in attached],
            "case": case_data,
            "steps": steps,
            "param": result.params,
            "defect": self.defect
        }

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

    def _create_run(self, plan_id = None, environment_id = None, cases: List = []) -> None:
        kwargs = dict(
                title=self.run_title,
                cases=cases,
                environment_id=(int(environment_id) if environment_id else None),
                plan_id=(int(plan_id) if plan_id else plan_id),
                is_autotest=True
        )
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
            prepared_step = {
                "time": step.execution.duration,
            }
            
            prepared_step["status"] = step.execution.status
            if step.execution.status == 'untested':
                prepared_step["status"] = 'passed'
            
            if step.step_type == "text":
                prepared_step['action'] = step.data.action
                if step.data.expected_result:
                    prepared_step['expected_result'] = step.data.expected_result
            
            if step.step_type == "request":
                prepared_step['action'] = step.data.request_method + " " + step.data.request_url
                if (step.data.request_body):
                    step.attachments.append(Attachment(file_name='request_body.txt', content=step.data.request_body, mime_type='text/plain', temporary=True))
                if (step.data.request_headers):
                    step.attachments.append(Attachment(file_name='request_headers.txt', content=step.data.request_headers, mime_type='text/plain', temporary=True))
                if (step.data.response_body):
                    step.attachments.append(Attachment(file_name='response_body.txt', content=step.data.response_body, mime_type='text/plain', temporary=True))
                if (step.data.response_headers):
                    step.attachments.append(Attachment(file_name='response_headers.txt', content=step.data.response_headers, mime_type='text/plain', temporary=True))

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
            self._create_run(plan_id = self.plan_id, environment_id = self.environment)
        if not self.run_id and not self.plan_id:
            self._create_run(environment_id = self.environment)
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
        if len(self.results) >= self.chunk_size:
            self._send_results()

    def get_results(self) -> List:
        return self.results + self.processed
    
    def set_results(self, results) -> None:
        self.results = results
