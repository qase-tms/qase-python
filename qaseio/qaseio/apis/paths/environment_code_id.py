from qaseio.paths.environment_code_id.get import ApiForget
from qaseio.paths.environment_code_id.delete import ApiFordelete
from qaseio.paths.environment_code_id.patch import ApiForpatch


class EnvironmentCodeId(
    ApiForget,
    ApiFordelete,
    ApiForpatch,
):
    pass
