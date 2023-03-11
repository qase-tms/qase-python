from qaseio.paths.case_code_id.get import ApiForget
from qaseio.paths.case_code_id.delete import ApiFordelete
from qaseio.paths.case_code_id.patch import ApiForpatch


class CaseCodeId(
    ApiForget,
    ApiFordelete,
    ApiForpatch,
):
    pass
