from typing import Optional

import attr

from . import helpers


@attr.s
class Reference:
    obj_id: str = attr.ib()
    target_type: Optional[str] = attr.ib()

    @classmethod
    def from_report(cls, report: dict):
        if report["_type"]["_name"] != "Reference":
            raise ValueError("type error")

        target_type: str = None
        if report.get("targetType") is not None:
            target_type = helpers.string_from_report(
                report["targetType"]["name"], dict(default=None)
            )

        return cls(helpers.string_from_report(report.get("id")), target_type)
