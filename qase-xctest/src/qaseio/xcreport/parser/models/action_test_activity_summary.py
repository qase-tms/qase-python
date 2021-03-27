from enum import Enum, unique
from typing import List

import attr

from . import helpers
from .action_test_attachment import ActionTestAttachment


@unique
class ActivityType(Enum):
    USER_CREATED = "com.apple.dt.xctest.activity-type.userCreated"
    FAILURE = "com.apple.dt.xctest.activity-type.testAssertionFailure"
    ATTACHMENT_CONTAINER = (
        "com.apple.dt.xctest.activity-type.attachmentContainer"
    )
    NONE = "none"


@attr.s
class ActionTestActivitySummary:
    title: str = attr.ib()
    activity_type: ActivityType = attr.ib()
    attachments: List[ActionTestAttachment] = attr.ib()
    subactivities: [] = attr.ib()  # ActionTestActivitySummary

    @classmethod
    def from_report(cls, report: dict):
        if report["_type"]["_name"] != "ActionTestActivitySummary":
            raise ValueError("type error")

        return cls(
            helpers.string_from_report(report.get("title")),
            helpers.enum_from_report(
                ActivityType,
                report.get("activityType"),
                dict(default=ActivityType.NONE),
            ),
            helpers.list_from_report(
                ActionTestAttachment,
                report.get("attachments"),
                dict(default=[]),
            ),
            helpers.list_from_report(
                ActionTestActivitySummary,
                report.get("subactivities"),
                dict(default=[]),
            ),
        )
