from enum import Enum, unique
from typing import List

import attr


@unique
class AccessLevel(Enum):
    ALL = "all"
    GROUP = "group"
    NONE = "none"


@unique
class Severity(Enum):
    UNDEFINED = "undefined"
    BLOCKER = "blocker"
    CRITICAL = "critical"
    MAJOR = "major"
    NORMAL = "normal"
    MINOR = "minor"
    TRIVIAL = "trivial"


@unique
class Priority(Enum):
    UNDEFINED = "undefined"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@unique
class Type(Enum):
    OTHER = "other"
    FUNCTIONAL = "functional"
    SMOKE = "smoke"
    REGRESSION = "regression"
    SECURITY = "security"
    USABILITY = "usability"
    PERFORMANCE = "performance"
    ACCEPTANCE = "acceptance"


@unique
class Behavior(Enum):
    UNDEFINED = "undefined"
    POSITIVE = "positive"
    NEGATIVE = "negative"
    DESTRUCTIVE = "destructive"


@unique
class Automation(Enum):
    IS_NOT_AUTOMATED = "is-not-automated"
    AUTOMATED = "automated"
    TO_BE_AUTOMATED = "to-be-automated"


@unique
class TestCaseStatus(Enum):
    ACTUAL = "actual"
    DRAFT = "draft"
    DEPRECATED = "deprecated"


@unique
class TestRunStatus(Enum):
    ACTIVE = "active"
    COMPLETE = "complete"
    ABORT = "abort"


@unique
class TestRunResultStatus(Enum):
    IN_PROGRESS = "in_progress"
    PASSED = "passed"
    FAILED = "failed"
    BLOCKED = "blocked"


class TestRunInclude:
    NONE = None
    CASES = "cases"


@attr.s
class DefaultList:
    total: int = attr.ib(default=None)
    filtered: int = attr.ib(default=None)
    count: int = attr.ib(default=None)


@attr.s
class DefaultFilter:
    _is_filter = True

    def _no_enum(self, value):
        if isinstance(value, Enum):
            return value.value
        return value

    def filter(self):
        from apitist.utils import is_sequence

        fields = attr.fields(type(self))
        filters = {}
        for field in fields:
            name = field.name
            values = getattr(self, field.name)
            if (
                values is not None
                and is_sequence(field.type)
                and isinstance(values, list)
            ):
                values = ",".join([self._no_enum(val) for val in values])
            else:
                values = self._no_enum(values)
            if values:
                filters[f"filters[{name}]"] = values
        return filters


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
class TestCaseFilters(DefaultFilter):
    search: str = attr.ib(default=None)
    milestone_id: int = attr.ib(default=None)
    suite_id: int = attr.ib(default=None)
    severity: List[Severity] = attr.ib(default=None)
    priority: List[Priority] = attr.ib(default=None)
    type: List[Type] = attr.ib(default=None)
    behavior: List[Behavior] = attr.ib(default=None)
    automation: List[Automation] = attr.ib(default=None)
    status: List[TestCaseStatus] = attr.ib(default=None)


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
class TestRunFilters(DefaultFilter):
    status: List[TestRunStatus] = attr.ib(default=None)


@attr.s
class TestRunList(DefaultList):
    entities: List[TestRunInfo] = attr.ib(factory=list)


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
    run_id = attr.ib(default=None)
    case_id = attr.ib(default=None)
    steps = attr.ib(factory=list)
    status = attr.ib(default=None)
    is_api_result = attr.ib(default=None)
    time_spent = attr.ib(default=None)
    end_time = attr.ib(default=None)


@attr.s
class TestRunResultList(DefaultList):
    entities: List[TestRunResultInfo] = attr.ib(factory=list)


@attr.s
class TestRunResultStepCreate:
    position: int = attr.ib()
    status: TestRunResultStatus = attr.ib()


@attr.s
class TestRunResultCreate:
    case_id: int = attr.ib()
    status: TestRunResultStatus = attr.ib()
    time: int = attr.ib(default=None)
    member_id: int = attr.ib(default=None)
    comment: str = attr.ib(default=None)
    defect: bool = attr.ib(default=None)
    steps: List[TestRunResultStepCreate] = attr.ib(factory=list)


@attr.s
class TestRunResultCreated:
    hash: str = attr.ib()


@attr.s
class TestRunResultUpdate:
    status: TestRunResultStatus = attr.ib(default=None)
    time: int = attr.ib(default=None)
    comment: str = attr.ib(default=None)
    defect: bool = attr.ib(default=None)
    steps: List[TestRunResultStepCreate] = attr.ib(factory=list)


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


@attr.s
class TestPlanCreated:
    id = attr.ib(default=None)
