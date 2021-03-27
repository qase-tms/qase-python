from typing import List

import attr

from . import helpers
from .action_test_summary_identifiable_object import (
    ActionTestSummaryIdentifiableObject,
)


@attr.s
class ActionTestSummaryGroup(ActionTestSummaryIdentifiableObject):
    subtests: List[ActionTestSummaryIdentifiableObject] = attr.ib()

    @classmethod
    def from_report(cls, report: dict):
        if report["_type"]["_name"] != "ActionTestSummaryGroup":
            raise ValueError("type error")

        return cls(
            cls.convert_name_field(report),
            cls.convert_identifier_field(report),
            helpers.list_from_report(
                ActionTestSummaryIdentifiableObject,
                report.get("subtests"),
                dict(default=[]),
            ),
        )


helpers.registry_subtype(
    ActionTestSummaryGroup, ActionTestSummaryIdentifiableObject
)
