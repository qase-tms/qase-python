from enum import Enum, unique
from typing import Optional

import attr

from . import helpers
from .reference import Reference


@unique
class UniformTypeIdentifier(Enum):
    PLAIN_TEXT = "public.plain-text"
    PNG = "public.png"


@attr.s
class ActionTestAttachment:
    type_identifier: Optional[UniformTypeIdentifier] = attr.ib()
    name: Optional[str] = attr.ib()
    payload_ref: Optional[Reference] = attr.ib()

    @classmethod
    def from_report(cls, report: dict):
        if report["_type"]["_name"] != "ActionTestAttachment":
            raise ValueError("type error")

        return cls(
            helpers.enum_from_report(
                UniformTypeIdentifier,
                report.get("uniformTypeIdentifier"),
                dict(default=None),
            ),
            helpers.string_from_report(report.get("name")),
            helpers.object_from_report(
                Reference, report.get("payloadRef"), dict(default=None)
            ),
        )
