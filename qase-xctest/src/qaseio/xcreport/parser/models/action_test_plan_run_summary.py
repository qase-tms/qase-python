from typing import List

import attr

from . import helpers
from .action_abstract_test_summary import ActionAbstractTestSummary
from .action_testable_summary import ActionTestableSummary


@attr.s
class ActionTestPlanRunSummary(ActionAbstractTestSummary):
    testable_summaries: List[ActionTestableSummary] = attr.ib()

    @classmethod
    def from_report(cls, report: dict):
        if report["_type"]["_name"] != "ActionTestPlanRunSummary":
            raise ValueError("type error")

        return cls(
            cls.convert_name_field(report),
            helpers.list_from_report(
                ActionTestableSummary,
                report.get("testableSummaries"),
                dict(default=[]),
            ),
        )
