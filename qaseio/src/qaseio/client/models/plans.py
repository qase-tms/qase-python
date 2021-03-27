from typing import List

import attr

from qaseio.client.models.base import DefaultList


@attr.s
class TestPlanCreate:
    title: str = attr.ib()
    cases: List[int] = attr.ib()
    description: str = attr.ib(default=None)

    @cases.validator
    def check(self, _, value):
        if not isinstance(value, list) or len(value) < 1:
            raise ValueError(
                "You should provide at least one test case for a run"
            )


@attr.s
class TestPlanUpdate(TestPlanCreate):
    title: str = attr.ib(default=None)
    cases: List[int] = attr.ib(factory=list)
    description: str = attr.ib(default=None)


@attr.s
class TestPlanCreated:
    id = attr.ib(default=None)


@attr.s
class TestPlanSteps:
    case_id = attr.ib(default=None)
    assignee_id = attr.ib(default=None)


@attr.s
class TestPlanInfo:
    id = attr.ib(default=None)
    title = attr.ib(default=None)
    description = attr.ib(default=None)
    cases_count = attr.ib(default=None)
    created = attr.ib(default=None)
    updated = attr.ib(default=None)
    average_time = attr.ib(default=None)
    cases: List[TestPlanSteps] = attr.ib(factory=list)


@attr.s
class TestPlanList(DefaultList):
    entities: List[TestPlanInfo] = attr.ib(factory=list)
