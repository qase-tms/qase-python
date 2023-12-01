from qaseio.utils.common import API_LIMIT, call_threaded
from qaseio.api.results_api import ResultsApi
from qaseio.utils.run import Run


class Result(Run):
    """Helper for ResultsApi"""

    def get_results(self, status=None, **data):
        """Get test results for selected test run"""

        all_results = []
        if "limit" not in data:
            data["limit"] = API_LIMIT
        if status:
            data["status"] = status
        one_data = data.copy()
        one_data["limit"] = 1
        number_of_results = self.get_result(
            ResultsApi(self.client).get_results(code=self.project, run=str(self.run_id), **one_data)
        )["filtered"]
        threads = []
        for offset in range(0, number_of_results, API_LIMIT):
            data["offset"] = offset
            thread = call_threaded(ResultsApi(self.client).get_results, code=self.project, run=str(self.run_id), **data)
            threads.append(thread)
        for thread in threads:
            response = thread.result()
            if results := response.result.entities:
                all_results.extend(results)
            else:
                break
        return all_results
