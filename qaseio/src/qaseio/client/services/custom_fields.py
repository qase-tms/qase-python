from typing import Union

from qaseio.client.models import CustomFieldInfo, CustomFieldList
from qaseio.client.services import BaseService, NotFoundException


class CustomFields(BaseService):
    def get_all(self, code: str, limit=None, offset=None):
        return self.vr(
            self.s.get(
                self.path("custom_field/{}".format(code)),
                params={"limit": limit, "offset": offset},
            ),
            to_type=CustomFieldList,
        )

    def get(self, code: str, field_id: Union[str, int]):
        return self.vr(
            self.s.get(self.path("custom_field/{}/{}".format(code, field_id))),
            to_type=CustomFieldInfo,
        )

    def exists(self, code: str, field_id: Union[str, int]):
        try:
            return self.get(code, field_id)
        except NotFoundException:
            return False
