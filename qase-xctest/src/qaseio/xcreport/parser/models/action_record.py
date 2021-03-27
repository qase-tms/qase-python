import attr

from . import helpers
from .action_result import ActionResult


@attr.s
class ActionRecord:
    action_result: ActionResult = attr.ib()

    @classmethod
    def from_report(cls, report: dict):
        if report["_type"]["_name"] != "ActionRecord":
            raise ValueError("type error")

        return cls(
            helpers.object_from_report(
                ActionResult, report.get("actionResult")
            )
        )
