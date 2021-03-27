from typing import List

import attr

from qaseio.client.models.base import DefaultFilter, DefaultList


@attr.s
class TestSuiteCreate:
    title: str = attr.ib()
    description: str = attr.ib(default=None)
    preconditions: str = attr.ib(default=None)
    parent_id: int = attr.ib(default=None)


@attr.s
class TestSuiteUpdate(TestSuiteCreate):
    title: str = attr.ib(default=None)


@attr.s
class TestSuiteCreated:
    id = attr.ib(default=None)


@attr.s
class TestSuiteInfo:
    id = attr.ib(default=None)
    title = attr.ib(default=None)
    description = attr.ib(default=None)
    preconditions = attr.ib(default=None)
    position: int = attr.ib(default=None)
    cases_count: int = attr.ib(default=None)
    parent_id: int = attr.ib(default=None)
    created = attr.ib(default=None)
    updated = attr.ib(default=None)


@attr.s
class TestSuiteList(DefaultList):
    entities: List[TestSuiteInfo] = attr.ib(factory=list)


@attr.s
class TestSuiteFilters(DefaultFilter):
    search: str = attr.ib(default=None)
