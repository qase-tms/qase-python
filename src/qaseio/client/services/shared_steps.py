from qaseio.client.models import (
    SharedStepCreate,
    SharedStepCreated,
    SharedStepFilters,
    SharedStepInfo,
    SharedStepList,
    SharedStepUpdate,
)
from qaseio.client.services import BaseService, NotFoundException


class SharedSteps(BaseService):
    def get_all(
        self,
        code: str,
        limit=None,
        offset=None,
        filters: SharedStepFilters = None,
    ):
        query = {"limit": limit, "offset": offset}
        if filters:
            query.update(filters.filter())
        return self.vr(
            self.s.get(self.path("shared_step/{}".format(code)), params=query),
            to_type=SharedStepList,
        )

    def get(self, code: str, shared_step_hash: str):
        return self.vr(
            self.s.get(
                self.path("shared_step/{}/{}".format(code, shared_step_hash))
            ),
            to_type=SharedStepInfo,
        )

    def create(self, code: str, data: SharedStepCreate):
        return self.vr(
            self.s.post(self.path("shared_step/{}".format(code)), data=data),
            to_type=SharedStepCreated,
        )

    def update(
        self, code: str, shared_step_hash: str, data: SharedStepUpdate,
    ):
        return self.vr(
            self.s.patch(
                self.path("shared_step/{}/{}".format(code, shared_step_hash)),
                data=data,
            ),
            to_type=SharedStepCreated,
        )

    def delete(self, code: str, shared_step_hash: str):
        return self.vr(
            self.s.delete(
                self.path("shared_step/{}/{}".format(code, shared_step_hash))
            ),
            to_type=None,
        )

    def exists(self, code: str, shared_step_hash: str):
        try:
            return self.get(code, shared_step_hash)
        except NotFoundException:
            return False
