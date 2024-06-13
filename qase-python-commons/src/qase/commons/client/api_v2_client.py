from typing import Dict

import certifi
from qase.api_client_v2 import ResultsApi
from qase.api_client_v2.api_client import ApiClient
from qase.api_client_v2.configuration import Configuration
from qase.api_client_v2.models.create_results_request_v2 import CreateResultsRequestV2
from qase.api_client_v2.models.relation_suite import RelationSuite
from qase.api_client_v2.models.relation_suite_item import RelationSuiteItem
from qase.api_client_v2.models.result_create import ResultCreate
from qase.api_client_v2.models.result_execution import ResultExecution
from qase.api_client_v2.models.result_relations import ResultRelations
from qase.api_client_v2.models.result_step_status import ResultStepStatus
from qase.api_client_v2.models.result_steps_type import ResultStepsType

from .api_v1_client import ApiV1Client
from .. import Logger
from ..exceptions.reporter import ReporterException
from ..models import Attachment, Result
from ..models.config.qaseconfig import QaseConfig
from ..models.step import StepType, Step


class ApiV2Client(ApiV1Client):
    def __init__(self, config: QaseConfig, logger: Logger):
        ApiV1Client.__init__(self, config, logger)

        try:
            self.logger.log_debug("Preparing API V2 client")
            configuration = Configuration()
            configuration.api_key['TokenAuth'] = self.config.testops.api.token
            configuration.ssl_ca_cert = certifi.where()
            host = self.config.testops.api.host
            if host == 'qase.io':
                configuration.host = f'https://api.{host}/v2'
                self.web = f'https://app.{host}'
            else:
                configuration.host = f'https://api-{host}/v2'
                self.web = f'https://{host}'

            self.client_v2 = ApiClient(configuration)
            self.logger.log_debug("API V2 client prepared")
        except Exception as e:
            self.logger.log(f"Error at preparing API V2 client: {e}", "error")
            raise ReporterException(e)

    def send_results(self, project_code: str, run_id: str, results: []) -> None:
        api_results = ResultsApi(self.client_v2)
        results_to_send = [self._prepare_result(project_code, result) for result in results]
        self.logger.log_debug(f"Sending results for run {run_id}: {results_to_send}")
        api_results.create_results_v2(project_code, run_id,
                                      create_results_request_v2=CreateResultsRequestV2(results=results_to_send))
        self.logger.log_debug(f"Results for run {run_id} sent successfully")

    def _prepare_result(self, project_code: str, result: Result) -> ResultCreate:
        attached = []
        if result.attachments:
            for attachment in result.attachments:
                attached.extend(self._upload_attachment(project_code, attachment))

        steps = []
        for step in result.steps:
            prepared = self._prepare_step(project_code, step)
            steps.append(prepared)

        for key, param in result.params.items():
            # Hack to match old TestOps API
            if param == "":
                result.params[key] = "empty"

        result_model_v2 = ResultCreate(
            title=result.get_title(),
            signature=result.signature,
            testops_id=result.get_testops_id(),
            execution=ResultExecution(start_time=result.execution.start_time, end_time=result.execution.end_time,
                                      status=result.execution.status, duration=result.execution.duration,
                                      stacktrace=result.execution.stacktrace, thread=result.execution.thread),
            fields=result.fields,
            attachments=[attach.hash for attach in attached],
            steps=steps,
            step_type=ResultStepsType.CLASSIC,
            params=result.params,
            muted=False,
            message=result.message,
        )

        if result.get_suite_title():
            data = []
            root_suite = self.config.root_suite
            if root_suite:
                data.append(RelationSuiteItem(title=root_suite))

            for suite in result.get_suite_title().split("."):
                data.append(RelationSuiteItem(title=suite))

            result_model_v2.relations = ResultRelations(suite=RelationSuite(data=data))

        self.logger.log_debug(f"Prepared result: {result_model_v2.to_json()}")

        return result_model_v2

    def _prepare_step(self, project_code: str, step: Step) -> Dict:
        prepared_children = []

        try:
            prepared_step = {'execution': {}, 'data': {}, 'steps': []}
            prepared_step['execution']['status'] = ResultStepStatus(step.execution.status)
            prepared_step['execution']['duration'] = step.execution.duration

            if step.step_type == StepType.TEXT:
                prepared_step['data']['action'] = step.data.action
                if step.data.expected_result:
                    prepared_step['data']['expected_result'] = step.data.expected_result

            if step.step_type == StepType.REQUEST:
                prepared_step['data']['action'] = step.data.request_method + " " + step.data.request_url

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
                prepared_step['data']['action'] = step.data.keyword

            if step.step_type == StepType.SLEEP:
                prepared_step['data']['action'] = f"Sleep for {step.data.duration} seconds"

            if step.attachments:
                uploaded_attachments = []
                for file in step.attachments:
                    uploaded_attachments.extend(self._upload_attachment(project_code, file))

                prepared_step['execution']['attachments'] = [attach.hash for attach in uploaded_attachments]

            if step.steps:
                for substep in step.steps:
                    prepared_children.append(self._prepare_step(project_code, substep))
                prepared_step['steps'] = prepared_children
            return prepared_step
        except Exception as e:
            self.logger.log(f"Error at preparing step: {e}", "error")
            raise ReporterException(e)
