from concurrent.futures import ThreadPoolExecutor

from qaseio.utils.common import API_LIMIT, get_result
from qaseio.api.results_api import ResultsApi
from qaseio.utils.run import Run


class Result(Run):
    """Helper for ResultsApi"""

    def __init__(self, project=None, parent_suite_id=None, token=None, run_id=None):
        super().__init__(project=project, parent_suite_id=parent_suite_id, token=token, run_id=run_id)
        self.results_api = ResultsApi(self.client)

    def get_results(self, status=None, last_result=True, **data):
        """
        Get test results for selected test run
        By default only the last result published in test run is considered.
        """

        all_results = []
        if "limit" not in data:
            data["limit"] = API_LIMIT
        if status and not last_result:
            data["status"] = status

        # Get number_of_results with limit=1 for faster response
        one_data = data.copy()
        one_data["limit"] = 1
        number_of_results = \
            get_result(self.results_api.get_results(code=self.project, run=str(self.run_id), **one_data))["filtered"]

        with ThreadPoolExecutor() as executor:
            data_iter = [(data, offset) for offset in range(0, number_of_results, API_LIMIT)]
            responses = list(executor.map(self._get_results, data_iter, timeout=5 * 60))
            for response in responses:
                if entities := get_result(response).entities:
                    all_results.extend(entities)
                else:
                    break
        if last_result:
            cases_results = {}
            for result in all_results:
                case_id = result["case_id"]
                if case_id not in cases_results or cases_results[case_id]["end_time"] < result["end_time"]:
                    cases_results[case_id] = result
            all_results = [result for _, result in cases_results.items()]
            if status:
                all_results = [result for result in all_results if result["status"].lower() == status.lower()]
        return all_results

    def _get_results(self, data_iter):
        data, offset = data_iter
        data["offset"] = offset
        return self.results_api.get_results(code=self.project, run=str(self.run_id), _request_timeout=60, **data)
