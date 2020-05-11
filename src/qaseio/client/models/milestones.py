from typing import List

import attr

from qaseio.client.models.base import DefaultFilter, DefaultList


@attr.s
class MilestoneCreate:
    title: str = attr.ib()
    description: str = attr.ib(default=None)


@attr.s
class MilestoneUpdate:
    title: str = attr.ib(default=None)
    description: str = attr.ib(default=None)


@attr.s
class MilestoneCreated:
    id = attr.ib(default=None)


@attr.s
class MilestoneInfo:
    id = attr.ib(default=None)
    title = attr.ib(default=None)
    description = attr.ib(default=None)
    due_date = attr.ib(default=None)
    created = attr.ib(default=None)
    updated = attr.ib(default=None)


@attr.s
class MilestoneList(DefaultList):
    entities: List[MilestoneInfo] = attr.ib(factory=list)


@attr.s
class MilestoneFilters(DefaultFilter):
    search: str = attr.ib(default=None)
