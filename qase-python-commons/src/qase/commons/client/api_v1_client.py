from datetime import datetime, timezone
from typing import Union

import certifi
from qase.api_client_v1 import ApiClient, ProjectsApi, Project, EnvironmentsApi, RunsApi, AttachmentsApi, \
    AttachmentGet, RunCreate
from qase.api_client_v1.configuration import Configuration
from .. import Logger
from .base_api_client import BaseApiClient
from ..exceptions.reporter import ReporterException
from ..models import Attachment
from ..models.config.framework import Video, Trace
from ..models.config.qaseconfig import QaseConfig


class ApiV1Client(BaseApiClient):
    def __init__(self, config: QaseConfig, logger: Logger):
        self.logger = logger
        self.config = config
        self.__authors = {}

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
            self.logger.log(f"Test run link: {self.web}/run/{project_code}/dashboard/{run_id}", "info")
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
            return None

    def create_test_run(self, project_code: str, title: str, description: str, plan_id=None,
                        environment_id=None) -> str:
        kwargs = dict(
            title=title,
            description=description,
            environment_id=(int(environment_id) if environment_id else None),
            plan_id=(int(plan_id) if plan_id else plan_id),
            is_autotest=True,
            start_time=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        )
        self.logger.log_debug(f"Creating test run with parameters: {kwargs}")
        try:
            result = RunsApi(self.client).create_run(
                code=project_code,
                run_create=RunCreate(**{k: v for k, v in kwargs.items() if v is not None})
            )

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

    def __should_skip_attachment(self, attachment, result):
        if (self.config.framework.playwright.video == Video.failed and
                result.execution.status != 'failed' and
                attachment.file_name == 'video.webm'):
            return True
        if (self.config.framework.playwright.trace == Trace.failed and
                result.execution.status != 'failed' and
                attachment.file_name == 'trace.zip'):
            return True
        return False

    def send_results(self, project_code: str, run_id: str, results: []) -> None:
        raise NotImplementedError("use ApiV2Client instead")
