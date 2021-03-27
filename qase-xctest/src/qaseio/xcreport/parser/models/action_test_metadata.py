from typing import Optional

import attr

from . import helpers
from .action_test_summary_identifiable_object import (
    ActionTestSummaryIdentifiableObject,
)
from .reference import Reference


@attr.s
class ActionTestMetadata(ActionTestSummaryIdentifiableObject):
    summary_ref: Optional[Reference] = attr.ib()

    @classmethod
    def from_report(cls, report: dict):
        if report["_type"]["_name"] != "ActionTestMetadata":
            raise ValueError("type error")

        return cls(
            cls.convert_name_field(report),
            cls.convert_identifier_field(report),
            helpers.object_from_report(
                Reference, report.get("summaryRef"), dict(default=None)
            ),
        )


helpers.registry_subtype(
    ActionTestMetadata, ActionTestSummaryIdentifiableObject
)
