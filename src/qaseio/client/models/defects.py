from enum import Enum, unique
from typing import List

import attr

from qaseio.client.models.base import DefaultFilter, DefaultList


@unique
class DefectStatus(Enum):
    OPEN = "open"
    RESOLVED = "resolved"


@attr.s
class DefectUpdated:
    id = attr.ib(default=None)


@attr.s
class DefectInfo:
    id = attr.ib(default=None)
    title = attr.ib(default=None)
    actual_result = attr.ib(default=None)
    status = attr.ib(default=None)
    user_id: int = attr.ib(default=None)
    attachments: List = attr.ib(factory=list)
    created = attr.ib(default=None)
    updated = attr.ib(default=None)


@attr.s
class DefectList(DefaultList):
    entities: List[DefectInfo] = attr.ib(factory=list)


@attr.s
class DefectFilters(DefaultFilter):
    status: DefectStatus = attr.ib(default=None)
