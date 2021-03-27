from enum import Enum, unique

import attr

from . import helpers
from .action_test_activity_summary import ActionTestActivitySummary
from .action_test_summary_identifiable_object import (
    ActionTestSummaryIdentifiableObject,
)


@unique
class TestStatus(Enum):
    FAULURE = "Failure"
    SUCCESS = "Success"
    UNDEFINE = "Undefine"


@attr.s
class ActionTestSummary(ActionTestSummaryIdentifiableObject):
    activity_summaries: [ActionTestActivitySummary] = attr.ib()
    duration: float = attr.ib()
    test_status: TestStatus = attr.ib()

    @classmethod
    def from_report(cls, report: dict):
        if report["_type"]["_name"] != "ActionTestSummary":
            raise ValueError("type error")

        return cls(
            cls.convert_name_field(report),
            cls.convert_identifier_field(report),
            helpers.list_from_report(
                ActionTestActivitySummary,
                report.get("activitySummaries"),
                dict(default=[]),
            ),
            helpers.float_from_report(report.get("duration")),
            helpers.enum_from_report(
                TestStatus,
                report.get("testStatus"),
                dict(default=TestStatus.UNDEFINE),
            ),
        )


helpers.registry_subtype(
    ActionTestSummary, ActionTestSummaryIdentifiableObject
)
