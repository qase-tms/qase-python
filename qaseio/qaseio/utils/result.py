import concurrent

from qaseio.utils.common import API_LIMIT, get_result
from qaseio.api.results_api import ResultsApi
from qaseio.utils.run import Run


class Result(Run):
    """Helper for ResultsApi"""

    def __init__(self, project=None, parent_suite_id=None, token=None, run_id=None):
        super().__init__(project=project, parent_suite_id=parent_suite_id, token=token)
        self.results_api = ResultsApi(self.client)

    def get_results(self, status=None, **data):
        """Get test results for selected test run"""

        all_results = []
        if "limit" not in data:
            data["limit"] = API_LIMIT
        if status:
            data["status"] = status
        one_data = data.copy()
        one_data["limit"] = 1
        number_of_results = \
        get_result(self.results_api.get_results(code=self.project, run=str(self.run_id), **one_data))["filtered"]

        with concurrent.futures.ThreadPoolExecutor() as executor:
            data_iter = [(data, offset) for offset in range(0, number_of_results, API_LIMIT)]
            responses = list(executor.map(self._get_results, data_iter, timeout=5 * 60))
            for response in responses:
                if entities := get_result(response).entities:
                    all_results.extend(entities)
                else:
                    break
        return all_results

    def _get_results(self, data_iter):
        data, offset = data_iter
        data["offset"] = offset
        return self.results_api.get_results(code=self.project, run=str(self.run_id), _request_timeout=60, **data)
