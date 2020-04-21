from qaseio.models import ProjectCreate
from qaseio.services import BaseService


class Projects(BaseService):

    def get_all(self, limit=None, offset=None):
        return self.vr(
            self.s.get(
                self.path("project"),
                params={"limit": limit, "offset": offset}
            )
        )

    def get(self, code: str):
        return self.vr(self.s.get(self.path("project/{}".format(code))))

    def create(self, data: ProjectCreate):
        return self.vr(self.s.post(self.path("project"), data=data))
