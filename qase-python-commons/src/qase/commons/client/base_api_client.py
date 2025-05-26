import abc
from typing import Union

from qase.api_client_v1 import Project, AttachmentGet

from ..models import Attachment


class BaseApiClient(abc.ABC):
    @abc.abstractmethod
    def get_project(self, project_code: str) -> Union[Project, None]:
        """
        Load a project from Qase TestOps by code and return project data

        :param project_code: project code
        :return: project data or None if project not found
        """

        pass

    @abc.abstractmethod
    def get_environment(self, environment: str, project_code: str) -> Union[str, None]:
        """
        Load an environment from Qase TestOps by name and returns environment id

        :param environment: environment name
        :param project_code: project code
        :return: environment id or None if environment not found
        """
        pass

    @abc.abstractmethod
    def complete_run(self, project_code: str, run_id: int) -> None:
        """
        Complete a test run in Qase TestOps

        :param project_code: project code
        :param run_id: test run id
        :return: None
        """
        pass

    @abc.abstractmethod
    def _upload_attachment(self, project_code: str, attachment: Attachment) -> Union[AttachmentGet, None]:
        """
        Upload an attachment to Qase TestOps

        :param project_code: project code
        :param attachment: attachment model
        :return: attachment data or None if attachment not uploaded
        """
        pass

    @abc.abstractmethod
    def create_test_run(self, project_code: str, title: str, description: str, plan_id=None,
                        environment_id=None) -> str:
        """
        Create a test run in Qase TestOps

        :param project_code: project code
        :param title: test run title
        :param description: test run description
        :param plan_id: plan id
        :param environment_id: environment id
        :return: test run id
        """
        pass

    @abc.abstractmethod
    def check_test_run(self, project_code: str, run_id: str) -> bool:
        """
        Check if test run exists in Qase TestOps
        :param project_code: project code
        :param run_id: test run id
        :return: True if test run exists, False otherwise
        """
        pass

    @abc.abstractmethod
    def send_results(self, project_code: str, run_id: str, results: []) -> None:
        """
        Send test results to Qase TestOps
        :param project_code: project code
        :param run_id: test run id
        :param results: results data
        :return: None
        """
        pass
