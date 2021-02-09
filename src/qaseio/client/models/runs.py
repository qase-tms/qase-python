from enum import Enum, unique
from typing import List

import attr

from qaseio.client.models.base import DefaultFilter, DefaultList


@unique
class TestRunStatus(Enum):
    ACTIVE = "active"
    COMPLETE = "complete"
    ABORT = "abort"


class TestRunInclude:
    NONE = None
    CASES = "cases"


@attr.s
class TestRunCreate:
    title: str = attr.ib()
    cases: List[int] = attr.ib()
    description: str = attr.ib(default=None)
    environment_id: int = attr.ib(default=None)

    @cases.validator
    def check(self, _, value):
        if value is not None and not isinstance(value, list):
            raise ValueError("You should provide list of cases or None")


@attr.s
class TestRunCreated:
    id = attr.ib(default=None)


@attr.s
class TestRunInfoStats:
    total = attr.ib(default=None)
    untested = attr.ib(default=None)
    passed = attr.ib(default=None)
    failed = attr.ib(default=None)
    blocked = attr.ib(default=None)
    skipped = attr.ib(default=None)
    retest = attr.ib(default=None)
    deleted = attr.ib(default=None)


@attr.s
class TestRunInfo:
    id = attr.ib(default=None)
    title = attr.ib(default=None)
    description = attr.ib(default=None)
    status = attr.ib(default=None)
    start_time = attr.ib(default=None)
    end_time = attr.ib(default=None)
    public = attr.ib(default=None)
    stats: TestRunInfoStats = attr.ib(default=None)
    time_spent = attr.ib(default=None)
    user_id = attr.ib(default=None)
    environment = attr.ib(default=None)
    cases = attr.ib(factory=list)


@attr.s
class TestRunFilters(DefaultFilter):
    status: List[TestRunStatus] = attr.ib(default=None)


@attr.s
class TestRunList(DefaultList):
    entities: List[TestRunInfo] = attr.ib(factory=list)
