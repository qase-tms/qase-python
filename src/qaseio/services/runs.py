from typing import Union

from qaseio.models import (
    TestRunCreate,
    TestRunCreated,
    TestRunInclude,
    TestRunInfo,
    TestRunList,
)
from qaseio.services import BaseService


class Runs(BaseService):
    def get_all(
        self, code: str, limit=None, offset=None, include=TestRunInclude.NONE
    ):
        return self.vr(
            self.s.get(
                self.path("run/{}".format(code)),
                params={"limit": limit, "offset": offset, "include": include},
            ),
            to_type=TestRunList,
        )

    def get(self, code: str, run_id: Union[str, int]):
        return self.vr(
            self.s.get(self.path("run/{}/{}".format(code, run_id))),
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
