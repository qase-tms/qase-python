from typing import Union

from qaseio.client.models import (
    MilestoneCreate,
    MilestoneCreated,
    MilestoneFilters,
    MilestoneInfo,
    MilestoneList,
    MilestoneUpdate,
)
from qaseio.client.services import BaseService, NotFoundException


class Milestones(BaseService):
    def get_all(
        self,
        code: str,
        limit=None,
        offset=None,
        filters: MilestoneFilters = None,
    ):
        query = {"limit": limit, "offset": offset}
        if filters:
            query.update(filters.filter())
        return self.vr(
            self.s.get(self.path("milestone/{}".format(code)), params=query),
            to_type=MilestoneList,
        )

    def get(self, code: str, suite_id: Union[str, int]):
        return self.vr(
            self.s.get(self.path("milestone/{}/{}".format(code, suite_id))),
            to_type=MilestoneInfo,
        )

    def create(self, code: str, data: MilestoneCreate):
        return self.vr(
            self.s.post(self.path("milestone/{}".format(code)), data=data),
            to_type=MilestoneCreated,
        )

    def update(
        self, code: str, suite_id: Union[str, int], data: MilestoneUpdate
    ):
        return self.vr(
            self.s.patch(
                self.path("milestone/{}/{}".format(code, suite_id)), data=data
            ),
            to_type=MilestoneCreated,
        )

    def delete(self, code: str, suite_id: Union[str, int]):
        return self.vr(
            self.s.delete(self.path("milestone/{}/{}".format(code, suite_id))),
            to_type=None,
        )

    def exists(self, code: str, suite_id: Union[str, int]):
        try:
            return self.get(code, suite_id)
        except NotFoundException:
            return False
