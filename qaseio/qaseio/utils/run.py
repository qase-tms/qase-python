import os
from qaseio.api.runs_api import RunsApi
from qaseio.utils.common import QaseClient, logger
from qaseio.utils.web.web import Web


class Run(QaseClient):
    """Helper for RunsApi"""

    def __init__(self, project=None, parent_suite_id=None, token=None, run_id=None):
        super().__init__(project=project, parent_suite_id=parent_suite_id, token=token)
        if not run_id:
            run_id = os.getenv("QASE_TESTOPS_RUN_ID")
            if not run_id:
                raise EnvironmentError("Set environment variable QASE_TESTOPS_RUN_ID or set `run_id` argument")
        self.run_id = run_id

    def get(self, **data):
        """Get run data for selected run id"""
        return self.get_result(RunsApi(self.client).get_run(code=self.project, id=self.run_id, **data))

    def get_cases(self):
        """Get all cases includes in the selected run"""
        return self.get(include="cases").cases

    def get_info(self):
        """
        Get run dashboard info by using Web api
        TODO: replace once qase api support getting configurations data
        """
        return Web().get_run_info(self.project, self.run_id)
