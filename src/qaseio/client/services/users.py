from typing import Union

from qaseio.client.models import UserInfo, UserList
from qaseio.client.services import BaseService, NotFoundException


class Users(BaseService):
    def get_all(self, limit=None, offset=None):
        return self.vr(
            self.s.get(
                self.path("user"), params={"limit": limit, "offset": offset}
            ),
            to_type=UserList,
        )

    def get(self, user_id: Union[str, int]):
        return self.vr(
            self.s.get(self.path("user/{}".format(user_id))),
            to_type=UserInfo,
        )

    def exists(self, code: str):
        try:
            return self.get(code)
        except NotFoundException:
            return False
