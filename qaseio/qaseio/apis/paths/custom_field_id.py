from qaseio.paths.custom_field_id.get import ApiForget
from qaseio.paths.custom_field_id.delete import ApiFordelete
from qaseio.paths.custom_field_id.patch import ApiForpatch


class CustomFieldId(
    ApiForget,
    ApiFordelete,
    ApiForpatch,
):
    pass
