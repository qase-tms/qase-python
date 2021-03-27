from qaseio.client.models import (
    ProjectCreate,
    ProjectCreated,
    ProjectInfo,
    ProjectList,
)
from qaseio.client.services import BaseService, NotFoundException


class Projects(BaseService):
    def get_all(self, limit=None, offset=None):
        return self.vr(
            self.s.get(
                self.path("project"), params={"limit": limit, "offset": offset}
            ),
            to_type=ProjectList,
        )

    def get(self, code: str):
        return self.vr(
            self.s.get(self.path("project/{}".format(code))),
            to_type=ProjectInfo,
        )

    def create(self, data: ProjectCreate):
        return self.vr(
            self.s.post(self.path("project"), data=data),
            to_type=ProjectCreated,
        )

    def exists(self, code: str):
        try:
            return self.get(code)
        except NotFoundException:
            return False
