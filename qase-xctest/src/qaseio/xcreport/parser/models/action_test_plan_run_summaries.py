from typing import List

import attr

from . import helpers
from .action_test_plan_run_summary import ActionTestPlanRunSummary


@attr.s
class ActionTestPlanRunSummaries:
    summaries: List[ActionTestPlanRunSummary] = attr.ib()

    @classmethod
    def from_report(cls, report: dict):
        if report["_type"]["_name"] != "ActionTestPlanRunSummaries":
            raise ValueError("type error")

        return cls(
            helpers.list_from_report(
                ActionTestPlanRunSummary,
                report.get("summaries"),
                dict(default=[]),
            )
        )
