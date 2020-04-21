from enum import Enum, unique

import attr


@unique
class AccessLevel(Enum):
    ALL = "all"
    GROUP = "group"
    NONE = "none"


@attr.s
class ProjectCreate:
    title: str = attr.ib()
    code: str = attr.ib()
    description: str = attr.ib(default=None)
    access: AccessLevel = attr.ib(default=AccessLevel.NONE)
    group: str = attr.ib(default=None)

    @code.validator
    def check(self, _, value):
        if not (2 <= len(value) <= 6) and not str(value).isascii():
            raise ValueError("code should be from 2 to 6 latin symbols")

    @group.validator
    def check(self, _, value):
        if self.access == AccessLevel.GROUP and not value:
            raise ValueError(
                "Group hash should be provided access group level"
            )
