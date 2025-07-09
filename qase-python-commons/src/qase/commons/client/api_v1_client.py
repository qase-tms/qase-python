from datetime import datetime, timezone
from typing import Union

import certifi
from qase.api_client_v1 import ApiClient, ProjectsApi, Project, EnvironmentsApi, RunsApi, AttachmentsApi, \
    AttachmentGet, RunCreate, ConfigurationsApi, ConfigurationCreate, ConfigurationGroupCreate
from qase.api_client_v1.configuration import Configuration
from .. import Logger
from .base_api_client import BaseApiClient
from ..exceptions.reporter import ReporterException
from ..models import Attachment
from ..models.config.framework import Video, Trace
from ..models.config.qaseconfig import QaseConfig
from ..models.config.testops import ConfigurationValue


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

    def get_configurations(self, project_code: str):
        """Get all configurations for the project"""
        try:
            self.logger.log_debug(f"Getting configurations for project {project_code}")
            api_instance = ConfigurationsApi(self.client)
            response = api_instance.get_configurations(code=project_code)
            if hasattr(response, 'result') and hasattr(response.result, 'entities'):
                return response.result.entities
            return []
        except Exception as e:
            self.logger.log(f"Exception when calling ConfigurationsApi->get_configurations: {e}", "error")
            return []

    def find_or_create_configuration(self, project_code: str, config_value: ConfigurationValue) -> Union[int, None]:
        """Find existing configuration or create new one if createIfNotExists is True"""
        try:
            configurations = self.get_configurations(project_code)
            
            # Search for existing configuration
            for group in configurations:
                if hasattr(group, 'configurations'):
                    for config in group.configurations:
                        # API returns configurations with 'title' field, not 'name' and 'value'
                        # We need to match group.title with config_value.name and config.title with config_value.value
                        config_title = config.title if hasattr(config, 'title') else 'No title'
                        group_title = group.title if hasattr(group, 'title') else 'No title'
                        
                        if (group_title == config_value.name and config_title == config_value.value):
                            return config.id
            
            # Configuration not found
            if not self.config.testops.configurations.create_if_not_exists:
                return None
            
            # Create new configuration
            # First, try to find existing group or create new one
            group_id = None
            for group in configurations:
                if hasattr(group, 'title') and group.title == config_value.name:
                    group_id = group.id
                    break
            
            if group_id is None:
                # Create new group
                group_create = ConfigurationGroupCreate(title=config_value.name)
                group_response = ConfigurationsApi(self.client).create_configuration_group(
                    code=project_code, 
                    configuration_group_create=group_create
                )
                group_id = group_response.result.id
            
            # Create configuration in the group
            config_create = ConfigurationCreate(
                title=config_value.value,
                group_id=group_id
            )
            config_response = ConfigurationsApi(self.client).create_configuration(
                code=project_code,
                configuration_create=config_create
            )
            config_id = config_response.result.id
            return config_id
            
        except Exception as e:
            self.logger.log(f"Error at finding/creating configuration {config_value.name}={config_value.value}: {e}", "error")
            return None

    def complete_run(self, project_code: str, run_id: int) -> None:
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
        # Process configurations
        configuration_ids = []
        
        if self.config.testops.configurations and self.config.testops.configurations.values:
            for config_value in self.config.testops.configurations.values:
                config_id = self.find_or_create_configuration(project_code, config_value)
                if config_id:
                    configuration_ids.append(config_id)
        
        kwargs = dict(
            title=title,
            description=description,
            environment_id=(int(environment_id) if environment_id else None),
            plan_id=(int(plan_id) if plan_id else plan_id),
            is_autotest=True,
            start_time=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
            tags=self.config.testops.run.tags
        )
        
        # Add configurations if any found
        if configuration_ids:
            kwargs['configurations'] = configuration_ids
        
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
