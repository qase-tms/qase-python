from typing import Union

from qaseio.client.models import (
    TestRunCreate,
    TestRunCreated,
    TestRunFilters,
    TestRunInclude,
    TestRunInfo,
    TestRunList,
)
from qaseio.client.services import BaseService, NotFoundException


class Runs(BaseService):
    def get_all(
        self,
        code: str,
        limit=None,
        offset=None,
        include=TestRunInclude.NONE,
        filters: TestRunFilters = None,
    ):
        query = {"limit": limit, "offset": offset, "include": include}
        if filters:
            query.update(filters.filter())
        return self.vr(
            self.s.get(self.path("run/{}".format(code)), params=query),
            to_type=TestRunList,
        )

    def get(
        self, code: str, run_id: Union[str, int], include=TestRunInclude.NONE
    ):
        query = {"include": include}
        return self.vr(
            self.s.get(
                self.path("run/{}/{}".format(code, run_id)), params=query
            ),
            to_type=TestRunInfo,
        )

    def create(self, code: str, data: TestRunCreate):
        return self.vr(
            self.s.post(self.path("run/{}".format(code)), data=data),
            to_type=TestRunCreated,
        )

    def delete(self, code: str, run_id: Union[str, int]):
        return self.vr(
            self.s.delete(self.path("run/{}/{}".format(code, run_id))),
            to_type=None,
        )

    def exists(self, code: str, run_id: Union[str, int], **kwargs):
        try:
            return self.get(code, run_id, **kwargs)
        except NotFoundException:
            return False
