from typing import Dict, Union

import certifi
from qase.api_client_v1 import ApiClient, ProjectsApi, Project, EnvironmentsApi, RunsApi, AttachmentsApi, \
    AttachmentGet, RunCreate, ResultsApi, ResultcreateBulk
from qase.api_client_v1.configuration import Configuration
from .. import Logger
from .base_api_client import BaseApiClient
from ..exceptions.reporter import ReporterException
from ..models import Attachment, Result, Step
from ..models.config.qaseconfig import QaseConfig
from ..models.step import StepType


class ApiV1Client(BaseApiClient):
    def __init__(self, config: QaseConfig, logger: Logger):
        self.logger = logger
        self.config = config

        try:
            self.logger.log_debug("Preparing API client")
            configuration = Configuration()
            configuration.api_key['TokenAuth'] = self.config.testops.api.token
            configuration.ssl_ca_cert = certifi.where()
            host = self.config.testops.api.host
            if host == 'qase.io':
                configuration.host = f'https://api.{host}/v1'
                self.web = f'https://app.{host}'
            else:
                configuration.host = f'https://api-{host}/v1'
                self.web = f'https://{host}'

            self.client = ApiClient(configuration)
            self.logger.log_debug("API client prepared")
        except Exception as e:
            self.logger.log(f"Error at preparing API client: {e}", "error")
            raise ReporterException(e)

    def get_project(self, project_code: str) -> Union[Project, None]:
        try:
            self.logger.log_debug(f"Getting project {project_code}")
            response = ProjectsApi(self.client).get_project(code=project_code)
            if hasattr(response, 'result'):
                self.logger.log_debug(f"Project {project_code} found: {response.result.to_json()}")
                return response.result
            raise ReporterException("Unable to find given project code")
        except Exception as e:
            self.logger.log("Exception when calling ProjectApi->get_project: %s\n" % e, "error")
            raise ReporterException("Exception when calling ProjectApi")

    def get_environment(self, environment: str, project_code: str) -> Union[str, None]:
        try:
            self.logger.log_debug(f"Getting environment {environment}")
            api_instance = EnvironmentsApi(self.client)
            response = api_instance.get_environments(code=project_code)
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

    def complete_run(self, project_code: str, run_id: str) -> None:
        api_runs = RunsApi(self.client)
        self.logger.log_debug(f"Completing run {run_id}")
        res = api_runs.get_run(project_code, run_id).result
        if res.status == 1:
            self.logger.log_debug(f"Run {run_id} already completed")
            return
        try:
            api_runs.complete_run(project_code, run_id)
            self.logger.log(f"Run {run_id} was completed successfully", "info")
        except Exception as e:
            self.logger.log(f"Error at completing run {run_id}: {e}", "error")
            raise ReporterException(e)

    def _upload_attachment(self, project_code: str, attachment: Attachment) -> Union[AttachmentGet, None]:
        try:
            self.logger.log_debug(f"Uploading attachment {attachment.id} for project {project_code}")
            attach_api = AttachmentsApi(self.client)
            response = attach_api.upload_attachment(project_code, file=[attachment.get_for_upload()])

            return response.result

        except Exception as e:
            self.logger.log(f"Error at uploading attachment: {e}", "error")
            raise ReporterException(e)

    def create_test_run(self, project_code: str, title: str, description: str, plan_id=None,
                        environment_id=None) -> str:
        kwargs = dict(
            title=title,
            description=description,
            environment_id=(int(environment_id) if environment_id else None),
            plan_id=(int(plan_id) if plan_id else plan_id),
            is_autotest=True
        )
        self.logger.log_debug(f"Creating test run with parameters: {kwargs}")
        try:
            result = RunsApi(self.client).create_run(
                code=project_code,
                run_create=RunCreate(**{k: v for k, v in kwargs.items() if v is not None})
            )

            self.logger.log(f"Test run was created: {self.web}/run/{project_code}/dashboard/{result.result.id}", "info")

            return result.result.id

        except Exception as e:
            self.logger.log(f"Error at creating test run: {e}", "error")
            raise ReporterException(e)

    def check_test_run(self, project_code: str, run_id: int) -> bool:
        api_runs = RunsApi(self.client)
        run = api_runs.get_run(code=project_code, id=run_id)
        if run.result.id:
            return True
        return False

    def send_results(self, project_code: str, run_id: str, results: []) -> None:
        api_results = ResultsApi(self.client)
        results_to_send = [self._prepare_result(project_code, result) for result in results]
        self.logger.log_debug(f"Sending results for run {run_id}: {results_to_send}")
        api_results.create_result_bulk(
            code=project_code,
            id=run_id,
            resultcreate_bulk=ResultcreateBulk(
                results=results_to_send
            )
        )
        self.logger.log_debug(f"Results for run {run_id} sent successfully")

    def _prepare_result(self, project_code: str, result: Result) -> Dict:
        attached = []
        if result.attachments:
            for attachment in result.attachments:
                attached.extend(self._upload_attachment(project_code, attachment))

        steps = []
        for step in result.steps:
            prepared = self._prepare_step(project_code, step)
            steps.append(prepared)

        case_data = {
            "title": result.get_title(),
            "description": result.get_field('description'),
            "preconditions": result.get_field('preconditions'),
            "postconditions": result.get_field('postconditions'),
        }

        for key, param in result.params.items():
            # Hack to match old TestOps API
            if param == "":
                result.params[key] = "empty"

        if result.get_field('severity'):
            case_data["severity"] = result.get_field('severity')

        if result.get_field('priority'):
            case_data["priority"] = result.get_field('priority')

        if result.get_field('layer'):
            case_data["layer"] = result.get_field('layer')

        suite = None
        if result.get_suite_title():
            suite = "\t".join(result.get_suite_title().split("."))

        root_suite = self.config.root_suite
        if root_suite:
            suite = f"{root_suite}\t{suite}"

        if suite:
            case_data["suite"] = suite

        result_model = {
            "status": result.execution.status,
            "stacktrace": result.execution.stacktrace,
            "time_ms": result.execution.duration,
            "comment": result.message,
            "attachments": [attach.hash for attach in attached],
            "steps": steps,
            "param": result.params,
            "defect": self.config.testops.defect,
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

    def _prepare_step(self, project_code: str, step: Step) -> Dict:
        prepared_children = []

        try:
            prepared_step = {"time": step.execution.duration, "status": step.execution.status}

            if step.execution.status == 'untested':
                prepared_step["status"] = 'passed'

            if step.execution.status == 'skipped':
                prepared_step["status"] = 'blocked'

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
                    uploaded_attachments.extend(self._upload_attachment(project_code, file))
                prepared_step['attachments'] = [attach.hash for attach in uploaded_attachments]

            if step.steps:
                for substep in step.steps:
                    prepared_children.append(self._prepare_step(project_code, substep))
                prepared_step["steps"] = prepared_children
            return prepared_step
        except Exception as e:
            self.logger.log(f"Error at preparing step: {e}", "error")
            raise ReporterException(e)
