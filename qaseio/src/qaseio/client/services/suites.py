from typing import Union

from qaseio.client.models import (
    TestSuiteCreate,
    TestSuiteCreated,
    TestSuiteFilters,
    TestSuiteInfo,
    TestSuiteList,
    TestSuiteUpdate,
)
from qaseio.client.services import BaseService, NotFoundException


class Suites(BaseService):
    def get_all(
        self,
        code: str,
        limit=None,
        offset=None,
        filters: TestSuiteFilters = None,
    ):
        query = {"limit": limit, "offset": offset}
        if filters:
            query.update(filters.filter())
        return self.vr(
            self.s.get(self.path("suite/{}".format(code)), params=query),
            to_type=TestSuiteList,
        )

    def get(self, code: str, suite_id: Union[str, int]):
        return self.vr(
            self.s.get(self.path("suite/{}/{}".format(code, suite_id))),
            to_type=TestSuiteInfo,
        )

    def create(self, code: str, data: TestSuiteCreate):
        return self.vr(
            self.s.post(self.path("suite/{}".format(code)), data=data),
            to_type=TestSuiteCreated,
        )

    def update(
        self, code: str, suite_id: Union[str, int], data: TestSuiteUpdate
    ):
        return self.vr(
            self.s.patch(
                self.path("suite/{}/{}".format(code, suite_id)), data=data
            ),
            to_type=TestSuiteCreated,
        )

    def delete(self, code: str, suite_id: Union[str, int]):
        return self.vr(
            self.s.delete(self.path("suite/{}/{}".format(code, suite_id))),
            to_type=None,
        )

    def exists(self, code: str, suite_id: Union[str, int]):
        try:
            return self.get(code, suite_id)
        except NotFoundException:
            return False
