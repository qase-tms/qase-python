from typing import List

import attr

from qaseio.client.models.base import DefaultFilter, DefaultList


@attr.s
class SharedStepCreate:
    title: str = attr.ib()
    action: str = attr.ib()
    expected_result: str = attr.ib(default=None)


@attr.s
class SharedStepUpdate:
    title: str = attr.ib(default=None)
    action: str = attr.ib(default=None)
    expected_result: str = attr.ib(default=None)


@attr.s
class SharedStepCreated:
    hash: str = attr.ib(default=None)


@attr.s
class SharedStepInfo:
    hash = attr.ib(default=None)
    title = attr.ib(default=None)
    action = attr.ib(default=None)
    expected_result = attr.ib(default=None)
    cases: List[int] = attr.ib(factory=list)
    cases_count: int = attr.ib(default=None)
    created = attr.ib(default=None)
    updated = attr.ib(default=None)


@attr.s
class SharedStepList(DefaultList):
    entities: List[SharedStepInfo] = attr.ib(factory=list)


@attr.s
class SharedStepFilters(DefaultFilter):
    search: str = attr.ib(default=None)
