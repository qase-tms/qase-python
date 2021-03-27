from typing import Union

from qaseio.client.models import (
    TestRunResultCreate,
    TestRunResultCreated,
    TestRunResultFilters,
    TestRunResultInfo,
    TestRunResultList,
    TestRunResultUpdate,
)
from qaseio.client.services import BaseService


class Results(BaseService):
    def get_all(
        self,
        code: str,
        limit=None,
        offset=None,
        filters: TestRunResultFilters = None,
    ):
        query = {"limit": limit, "offset": offset}
        if filters:
            query.update(filters.filter())
        return self.vr(
            self.s.get(self.path("result/{}".format(code)), params=query),
            to_type=TestRunResultList,
        )

    def get(self, code: str, hash: str):
        return self.vr(
            self.s.get(self.path("result/{}/{}".format(code, hash))),
            to_type=TestRunResultInfo,
        )

    def create(
        self, code: str, run_id: Union[str, int], data: TestRunResultCreate
    ):
        return self.vr(
            self.s.post(
                self.path("result/{}/{}".format(code, run_id)), data=data
            ),
            to_type=TestRunResultCreated,
        )

    def update(
        self,
        code: str,
        run_id: Union[str, int],
        hash: str,
        data: TestRunResultUpdate,
    ):
        return self.vr(
            self.s.patch(
                self.path("result/{}/{}/{}".format(code, run_id, hash)),
                data=data,
            ),
            to_type=TestRunResultCreated,
        )

    def delete(self, code: str, run_id: Union[str, int], hash: str):
        return self.vr(
            self.s.delete(
                self.path("result/{}/{}/{}".format(code, run_id, hash))
            ),
            to_type=None,
        )
