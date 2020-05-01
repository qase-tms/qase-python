from typing import Union

from qaseio.models import TestCaseInfo, TestCaseList
from qaseio.services import BaseService


class TestCases(BaseService):
    def get_all(self, code: str, limit=None, offset=None):
        return self.vr(
            self.s.get(
                self.path("case/{}".format(code)),
                params={"limit": limit, "offset": offset},
            ),
            to_type=TestCaseList,
        )

    def get(self, code: str, case_id: Union[str, int]):
        return self.vr(
            self.s.get(self.path("case/{}/{}".format(code, case_id))),
            to_type=TestCaseInfo,
        )

    def delete(self, code: str, case_id: Union[str, int]):
        return self.vr(
            self.s.delete(self.path("case/{}/{}".format(code, case_id))),
            to_type=None,
        )
