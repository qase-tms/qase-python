from enum import Enum, unique
from typing import List

import attr


@unique
class AccessLevel(Enum):
    ALL = "all"
    GROUP = "group"
    NONE = "none"


class TestRunInclude:
    NONE = None
    CASES = "cases"


@attr.s
class ProjectCreate:
    title: str = attr.ib()
    code: str = attr.ib(
        validator=[
            attr.validators.instance_of(str),
            attr.validators.matches_re(r"[a-zA-Z]{2,6}"),
        ]
    )
    description: str = attr.ib(default=None)
    access: AccessLevel = attr.ib(default=AccessLevel.NONE)
    group: str = attr.ib(default=None)

    @group.validator
    def check(self, _, value):
        if self.access == AccessLevel.GROUP and not value:
            raise ValueError(
                "Group hash should be provided access group level"
            )


@attr.s
class ProjectCreated:
    code = attr.ib(default=None)


@attr.s
class ProjectCountsRuns:
    total = attr.ib(default=None)
    active = attr.ib(default=None)


@attr.s
class ProjectCountsDefects:
    total = attr.ib(default=None)
    open = attr.ib(default=None)


@attr.s
class ProjectCounts:
    cases = attr.ib(default=None)
    suites = attr.ib(default=None)
    milestones = attr.ib(default=None)
    runs: ProjectCountsRuns = attr.ib(default=None)
    defects: ProjectCountsDefects = attr.ib(default=None)


@attr.s
class ProjectInfo:
    title = attr.ib(default=None)
    code = attr.ib(default=None)
    counts: ProjectCounts = attr.ib(default=None)


@attr.s
class DefaultList:
    total: int = attr.ib(default=None)
    filtered: int = attr.ib(default=None)
    count: int = attr.ib(default=None)


@attr.s
class ProjectList(DefaultList):
    entities: List[ProjectInfo] = attr.ib(factory=list)


@attr.s
class TestCaseInfo:
    id = attr.ib(default=None)
    position = attr.ib(default=None)
    title = attr.ib(default=None)
    description = attr.ib(default=None)
    preconditions = attr.ib(default=None)
    postconditions = attr.ib(default=None)
    severity = attr.ib(default=None)
    priority = attr.ib(default=None)
    type = attr.ib(default=None)
    behavior = attr.ib(default=None)
    automation = attr.ib(default=None)
    status = attr.ib(default=None)
    milestone_id = attr.ib(default=None)
    suite_id = attr.ib(default=None)
    tags = attr.ib(factory=list)
    links = attr.ib(factory=list)
    revision = attr.ib(default=None)
    custom_fields = attr.ib(factory=list)
    attachments = attr.ib(factory=list)
    steps = attr.ib(factory=list)
    created = attr.ib(default=None)
    updated = attr.ib(default=None)


@attr.s
class TestCaseList(DefaultList):
    entities: List[TestCaseInfo] = attr.ib(factory=list)


@attr.s
class TestRunCreate:
    title: str = attr.ib()
    cases: List[int] = attr.ib()
    description: str = attr.ib(default=None)
    environment_id: int = attr.ib(default=None)

    @cases.validator
    def check(self, _, value):
        if not isinstance(value, list) or len(value) < 1:
            raise ValueError(
                "You should provide at least one test case for a run"
            )


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
class TestRunList(DefaultList):
    entities: List[TestRunInfo] = attr.ib(factory=list)
