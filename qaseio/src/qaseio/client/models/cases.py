from enum import Enum, unique
from typing import List

import attr

from qaseio.client.models.base import (
    Automation,
    Behavior,
    DefaultFilter,
    DefaultList,
    Priority,
    Severity,
    Type,
)


@unique
class TestCaseStatus(Enum):
    ACTUAL = "actual"
    DRAFT = "draft"
    DEPRECATED = "deprecated"


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
