from qaseio.paths.defect_code_id.get import ApiForget
from qaseio.paths.defect_code_id.delete import ApiFordelete
from qaseio.paths.defect_code_id.patch import ApiForpatch


class DefectCodeId(
    ApiForget,
    ApiFordelete,
    ApiForpatch,
):
    pass
