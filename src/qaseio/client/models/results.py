from enum import Enum, unique
from typing import List

import attr

from qaseio.client.models.base import DefaultFilter, DefaultList


@unique
class TestRunResultStatus(Enum):
    IN_PROGRESS = "in_progress"
    PASSED = "passed"
    FAILED = "failed"
    BLOCKED = "blocked"


@attr.s
class TestRunResultFilters(DefaultFilter):
    status: List[TestRunResultStatus] = attr.ib(default=None)
    member: int = attr.ib(default=None)
    run: int = attr.ib(default=None)
    case_id: int = attr.ib(default=None)
    from_end_time: str = attr.ib(default=None)
    to_end_time: str = attr.ib(default=None)


@attr.s
class TestRunResultInfo:
    hash = attr.ib(default=None)
    comment = attr.ib(default=None)
    stacktrace = attr.ib(default=None)
    run_id = attr.ib(default=None)
    case_id = attr.ib(default=None)
    steps = attr.ib(factory=list)
    status = attr.ib(default=None)
    is_api_result = attr.ib(default=None)
    time_spent = attr.ib(default=None)
    end_time = attr.ib(default=None)
    attachments: List[str] = attr.ib(factory=list)


@attr.s
class TestRunResultList(DefaultList):
    entities: List[TestRunResultInfo] = attr.ib(factory=list)


@attr.s
class TestRunResultStepCreate:
    position: int = attr.ib()
    status: TestRunResultStatus = attr.ib()
    attachments: List[str] = attr.ib(factory=list)
    comment: str = attr.ib(default=None)


@attr.s
class TestRunResultCreate:
    case_id: int = attr.ib()
    status: TestRunResultStatus = attr.ib()
    time: int = attr.ib(default=None)
    member_id: int = attr.ib(default=None)
    comment: str = attr.ib(default=None)
    stacktrace: str = attr.ib(default=None)
    defect: bool = attr.ib(default=None)
    steps: List[TestRunResultStepCreate] = attr.ib(factory=list)
    attachments: List[str] = attr.ib(factory=list)


@attr.s
class TestRunResultCreated:
    hash: str = attr.ib()


@attr.s
class TestRunResultUpdate:
    status: TestRunResultStatus = attr.ib(default=None)
    time: int = attr.ib(default=None)
    comment: str = attr.ib(default=None)
    stacktrace: str = attr.ib(default=None)
    defect: bool = attr.ib(default=None)
    steps: List[TestRunResultStepCreate] = attr.ib(factory=list)
    attachments: List[str] = attr.ib(factory=list)
