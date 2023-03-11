from qaseio.paths.shared_step_code_hash.get import ApiForget
from qaseio.paths.shared_step_code_hash.delete import ApiFordelete
from qaseio.paths.shared_step_code_hash.patch import ApiForpatch


class SharedStepCodeHash(
    ApiForget,
    ApiFordelete,
    ApiForpatch,
):
    pass
