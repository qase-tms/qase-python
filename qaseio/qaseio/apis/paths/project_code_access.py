from qaseio.paths.project_code_access.post import ApiForpost
from qaseio.paths.project_code_access.delete import ApiFordelete


class ProjectCodeAccess(
    ApiForpost,
    ApiFordelete,
):
    pass
