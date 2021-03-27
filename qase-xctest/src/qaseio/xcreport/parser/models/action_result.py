from typing import Optional

import attr

from . import helpers
from .reference import Reference


@attr.s
class ActionResult:
    tests_ref: Optional[Reference] = attr.ib()

    @classmethod
    def from_report(cls, report: dict):
        if report["_type"]["_name"] != "ActionResult":
            raise ValueError("type error")

        return cls(
            helpers.object_from_report(
                Reference, report.get("testsRef"), dict(default=None)
            )
        )
