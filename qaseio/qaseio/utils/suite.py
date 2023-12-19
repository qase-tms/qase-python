import functools
from concurrent.futures import ThreadPoolExecutor

from qaseio.api.cases_api import CasesApi
from qaseio.api.suites_api import SuitesApi
from qaseio.utils.common import (
    MAX_NUMBER_OF_SUITES,
    API_LIMIT,
    QaseClient,
    get_result,
)


class Suite(QaseClient):
    """Helper for SuitesApi"""

    def __init__(self, project=None, parent_suite_id=None, token=None):
        super().__init__(project=project, parent_suite_id=parent_suite_id, token=token)
        self.suites_api = SuitesApi(self.client)
        self.cases_api = CasesApi(self.client)

    def get_cases(self):
        """Get cases included in specified parent suite id"""
        counted_cases = self.count_cases()
        data = {"limit": API_LIMIT}
        all_cases = []
        if counted_cases < 100:
            suites = self.all
        else:
            suites = [{"id": None, "cases_count": self.count_cases(self.all_project_suites)}]
        for suite in suites:
            suite_id = suite["id"]
            case_count = suite["cases_count"]
            if not case_count:
                continue
            if suite_id:
                data["suite_id"] = suite_id

            suites_ids = self.get_ids()

            with ThreadPoolExecutor() as executor:
                data_iter = [(data, offset) for offset in range(0, case_count, API_LIMIT)]
                responses = list(executor.map(self._get_cases, data_iter, timeout=5 * 60))
                for response in responses:
                    ret = get_result(response)
                    if ret.count == 0:
                        continue
                    for case in ret.entities:
                        if case.suite_id in suites_ids:
                            all_cases.append(case)

        if len(all_cases) != counted_cases:
            raise RuntimeError("Not all cases where successfully collected")
        return all_cases

    def _get_cases(self, data_iter):
        data, offset = data_iter
        data["offset"] = offset
        return self.cases_api.get_cases(code=self.project, _request_timeout=60, **data)

    @functools.cached_property
    def all_project_suites(self):
        """Get all project suites"""
        all_suites = []
        data = {"limit": API_LIMIT}

        with ThreadPoolExecutor() as executor:
            data_iter = [(data, offset) for offset in range(0, MAX_NUMBER_OF_SUITES, API_LIMIT)]
            responses = list(executor.map(self._get_suites, data_iter, timeout=5 * 60))
            for response in responses:
                ret = get_result(response)
                for suite in ret.entities:
                    all_suites.append(
                        {
                            "parent_id": suite["parent_id"],
                            "id": suite["id"],
                            "title": suite["title"],
                            "cases_count": suite["cases_count"],
                        }
                    )
        return all_suites

    def _get_suites(self, data_iter):
        data, offset = data_iter
        data["offset"] = offset
        return self.suites_api.get_suites(code=self.project, _request_timeout=60, **data)

    @functools.cached_property
    def parent_suite(self):
        """Get parent suite with children"""
        all_project_suites = self.all_project_suites

        parent_suites = {}
        for suite in all_project_suites:
            if "childs" not in suite:
                suite["childs"] = []
            parent_suite = suite["parent_id"]
            suite_id = suite["id"]
            if parent_suite is None:
                parent_suites[suite_id] = suite
            else:
                if parent_suite not in parent_suites:
                    parent_suites[parent_suite] = next(
                        _suite for _suite in all_project_suites if _suite["id"] == parent_suite
                    )
                    parent_suites[parent_suite]["childs"] = []
                parent_suites[parent_suite]["childs"].append(suite)
                if suite_id not in parent_suites:
                    parent_suites[suite_id] = suite
        parent_suite_id = self.parent_suite_id if self.parent_suite_id else list(parent_suites.keys())[0]
        return parent_suites[parent_suite_id]

    @functools.cached_property
    def all(self):
        """Get parent suites and all child suites data"""
        return Suite._get_suite_details(suite=self.parent_suite)

    @staticmethod
    def _get_suite_details(suite, details=None):
        if details is None:
            details = []
        details.append({"id": suite["id"], "cases_count": suite["cases_count"]})
        for child in suite["childs"]:
            Suite._get_suite_details(child, details)
        return details

    def count_cases(self, suites=None):
        """Count all cases in parent suite and its children"""
        count_cases = 0
        if suites is None:
            suites = self.all
        for suite_data in suites:
            count_cases += suite_data["cases_count"]
        return count_cases

    def get_ids(self):
        """Get all suites ids for parent suite and its children"""
        suites_ids = set()
        for suite_data in self.all:
            suites_ids.add(suite_data["id"])
        return suites_ids
