from typing import Optional

import attr

from . import helpers


@attr.s
class ActionAbstractTestSummary:
    name: Optional[str] = attr.ib()

    @classmethod
    def convert_name_field(cls, report: dict) -> Optional[str]:
        return helpers.string_from_report(
            report.get("name"), dict(default=None)
        )
