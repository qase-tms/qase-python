from typing import List

import attr

from qaseio.client.models.base import AccessLevel, DefaultList


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
