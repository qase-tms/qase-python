from qaseio.paths.milestone_code_id.get import ApiForget
from qaseio.paths.milestone_code_id.delete import ApiFordelete
from qaseio.paths.milestone_code_id.patch import ApiForpatch


class MilestoneCodeId(
    ApiForget,
    ApiFordelete,
    ApiForpatch,
):
    pass
