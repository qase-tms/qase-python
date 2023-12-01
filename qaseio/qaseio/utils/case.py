from qaseio.api.cases_api import CasesApi
from qaseio.utils.common import QaseClient


class Case(QaseClient):
    """Helper for CasesApi"""

    def __init__(self, case_id, project=None, parent_suite_id=None, token=None):
        super().__init__(project, parent_suite_id, token)
        self.case_id = case_id

    def get(self):
        """Get a single case"""
        return self.get_result(CasesApi(self.client).get_case(code=self.project, id=self.case_id))
