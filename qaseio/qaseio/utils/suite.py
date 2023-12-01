import functools

from qaseio.api.cases_api import CasesApi
from qaseio.utils.common import MAX_NUMBER_OF_SUITES, API_LIMIT, call_threaded, QaseClient, logger
from qaseio.api.suites_api import SuitesApi


class Suite(QaseClient):
    """Helper for RunsApi"""

    def get_cases(self):
        """Get cases included in specified parent suite id"""
        logger.info(
            f"Fetching: %s cases for qaseio project: %s, parent_suite_id: %s",
            self.count_cases(),
            self.project,
            self.parent_suite_id,
        )
        data = {"limit": API_LIMIT}
        all_cases = []
        if self.count_cases() < 100:
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
            threads = []
            for offset in range(0, case_count, API_LIMIT):
                data["offset"] = offset
                thread = call_threaded(CasesApi(self.client).get_cases, code=self.project, **data)
                threads.append(thread)
            for thread in threads:
                ret = thread.result().result
                if ret.count == 0:
                    continue
                for case in ret.entities:
                    if case.suite_id in self.get_ids():
                        all_cases.append(case)

        if len(all_cases) != self.count_cases():
            raise RuntimeError("Not all cases where successfully collected")
        return all_cases

    @functools.cached_property
    def all_project_suites(self):
        """Get all project suites"""
        threads = []
        all_suites = []
        data = {"limit": API_LIMIT}

        suites_api = SuitesApi(self.client)

        for suite in range(0, MAX_NUMBER_OF_SUITES, API_LIMIT):
            data["offset"] = suite
            thread = call_threaded(suites_api.get_suites, code=self.project, **data)
            threads.append(thread)
        for thread in threads:
            ret = thread.result().result
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
