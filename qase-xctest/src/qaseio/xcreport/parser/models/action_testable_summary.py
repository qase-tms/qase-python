from typing import List

import attr

from . import helpers
from .action_abstract_test_summary import ActionAbstractTestSummary
from .action_test_summary_identifiable_object import (
    ActionTestSummaryIdentifiableObject,
)


@attr.s
class ActionTestableSummary(ActionAbstractTestSummary):
    tests: List[ActionTestSummaryIdentifiableObject] = attr.ib()

    @classmethod
    def from_report(cls, report: dict):
        if report["_type"]["_name"] != "ActionTestableSummary":
            raise ValueError("type error")

        return cls(
            cls.convert_name_field(report),
            helpers.list_from_report(
                ActionTestSummaryIdentifiableObject,
                report.get("tests"),
                dict(default=[]),
            ),
        )
