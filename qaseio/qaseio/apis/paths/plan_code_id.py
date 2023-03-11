from qaseio.paths.plan_code_id.get import ApiForget
from qaseio.paths.plan_code_id.delete import ApiFordelete
from qaseio.paths.plan_code_id.patch import ApiForpatch


class PlanCodeId(
    ApiForget,
    ApiFordelete,
    ApiForpatch,
):
    pass
