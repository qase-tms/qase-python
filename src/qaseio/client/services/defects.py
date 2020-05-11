from typing import Union

from qaseio.client.models import (
    DefectFilters,
    DefectInfo,
    DefectList,
    DefectUpdated,
)
from qaseio.client.services import BaseService, NotFoundException


class Defects(BaseService):
    def get_all(
        self,
        code: str,
        limit=None,
        offset=None,
        filters: DefectFilters = None,
    ):
        query = {"limit": limit, "offset": offset}
        if filters:
            query.update(filters.filter())
        return self.vr(
            self.s.get(self.path("defect/{}".format(code)), params=query),
            to_type=DefectList,
        )

    def get(self, code: str, defect_id: Union[str, int]):
        return self.vr(
            self.s.get(self.path("defect/{}/{}".format(code, defect_id))),
            to_type=DefectInfo,
        )

    def resolve(self, code: str, defect_id: Union[str, int]):
        return self.vr(
            self.s.patch(
                self.path("defect/{}/resolve/{}".format(code, defect_id))
            ),
            to_type=DefectUpdated,
        )

    def delete(self, code: str, defect_id: Union[str, int]):
        return self.vr(
            self.s.delete(self.path("defect/{}/{}".format(code, defect_id))),
            to_type=None,
        )

    def exists(self, code: str, defect_id: Union[str, int]):
        try:
            return self.get(code, defect_id)
        except NotFoundException:
            return False
