from typing import Union

from qaseio.client.models import (
    TestPlanCreate,
    TestPlanCreated,
    TestPlanInfo,
    TestPlanList,
    TestPlanUpdate,
)
from qaseio.client.services import BaseService, NotFoundException


class Plans(BaseService):
    def get_all(
        self, code: str, limit=None, offset=None,
    ):
        query = {"limit": limit, "offset": offset}
        return self.vr(
            self.s.get(self.path("plan/{}".format(code)), params=query),
            to_type=TestPlanList,
        )

    def get(self, code: str, plan_id: Union[str, int]):
        return self.vr(
            self.s.get(self.path("plan/{}/{}".format(code, plan_id))),
            to_type=TestPlanInfo,
        )

    def create(self, code: str, data: TestPlanCreate):
        return self.vr(
            self.s.post(self.path("plan/{}".format(code)), data=data),
            to_type=TestPlanCreated,
        )

    def update(
        self, code: str, plan_id: Union[str, int], data: TestPlanUpdate
    ):
        return self.vr(
            self.s.patch(
                self.path("plan/{}/{}".format(code, plan_id)), data=data
            ),
            to_type=TestPlanCreated,
        )

    def delete(self, code: str, plan_id: Union[str, int]):
        return self.vr(
            self.s.delete(self.path("plan/{}/{}".format(code, plan_id))),
            to_type=None,
        )

    def exists(self, code: str, plan_id: Union[str, int]):
        try:
            return self.get(code, plan_id)
        except NotFoundException:
            return False
