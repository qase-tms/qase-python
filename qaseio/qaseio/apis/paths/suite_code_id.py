from qaseio.paths.suite_code_id.get import ApiForget
from qaseio.paths.suite_code_id.delete import ApiFordelete
from qaseio.paths.suite_code_id.patch import ApiForpatch


class SuiteCodeId(
    ApiForget,
    ApiFordelete,
    ApiForpatch,
):
    pass
