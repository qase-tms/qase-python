from typing import List

import attr

from qaseio.client.models.base import DefaultList


@attr.s
class UserInfo:
    id = attr.ib(default=None)
    name = attr.ib(default=None)
    email = attr.ib(default=None)
    title = attr.ib(default=None)
    status: int = attr.ib(default=None)


@attr.s
class UserList(DefaultList):
    entities: List[UserInfo] = attr.ib(factory=list)
