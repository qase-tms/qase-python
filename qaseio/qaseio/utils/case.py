from qaseio.api.cases_api import CasesApi
from qaseio.model.test_case_update import TestCaseUpdate
from qaseio.utils.common import QaseClient, api_result


class Case(QaseClient):
    """Helper for CasesApi"""

    def __init__(
        self, case_id: int, project: str | None = None, parent_suite_id: int | None = None, token: int | None = None
    ):
        super().__init__(project, parent_suite_id, token)
        self.case_id = case_id

    @api_result
    def get(self):
        """Get a single case"""
        return CasesApi(self.client).get_case(code=self.project, id=self.case_id)

    @api_result
    def update(self, test_case_update: TestCaseUpdate):
        return CasesApi(self.client).update_case(code=self.project, id=self.case_id, test_case_update=test_case_update)
