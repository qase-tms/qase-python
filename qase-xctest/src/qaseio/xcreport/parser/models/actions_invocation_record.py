from typing import List

import attr

from . import helpers
from .action_record import ActionRecord


@attr.s
class ActionsInvocationRecord:
    actions: List[ActionRecord] = attr.ib()

    @classmethod
    def from_report(cls, report: dict):
        if report["_type"]["_name"] != "ActionsInvocationRecord":
            raise ValueError("type error")

        return cls(
            helpers.list_from_report(
                ActionRecord, report.get("actions"), dict(default=[])
            )
        )
