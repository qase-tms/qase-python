import typing_extensions

from qaseio.paths import PathValues
from qaseio.apis.paths.attachment import Attachment
from qaseio.apis.paths.attachment_code import AttachmentCode
from qaseio.apis.paths.attachment_hash import AttachmentHash
from qaseio.apis.paths.author import Author
from qaseio.apis.paths.author_id import AuthorId
from qaseio.apis.paths.case_code import CaseCode
from qaseio.apis.paths.case_code_id import CaseCodeId
from qaseio.apis.paths.custom_field import CustomField
from qaseio.apis.paths.custom_field_id import CustomFieldId
from qaseio.apis.paths.defect_code import DefectCode
from qaseio.apis.paths.defect_code_id import DefectCodeId
from qaseio.apis.paths.defect_code_resolve_id import DefectCodeResolveId
from qaseio.apis.paths.defect_code_status_id import DefectCodeStatusId
from qaseio.apis.paths.environment_code import EnvironmentCode
from qaseio.apis.paths.environment_code_id import EnvironmentCodeId
from qaseio.apis.paths.milestone_code import MilestoneCode
from qaseio.apis.paths.milestone_code_id import MilestoneCodeId
from qaseio.apis.paths.plan_code import PlanCode
from qaseio.apis.paths.plan_code_id import PlanCodeId
from qaseio.apis.paths.project import Project
from qaseio.apis.paths.project_code import ProjectCode
from qaseio.apis.paths.project_code_access import ProjectCodeAccess
from qaseio.apis.paths.result_code import ResultCode
from qaseio.apis.paths.result_code_id import ResultCodeId
from qaseio.apis.paths.result_code_hash import ResultCodeHash
from qaseio.apis.paths.result_code_id_bulk import ResultCodeIdBulk
from qaseio.apis.paths.result_code_id_hash import ResultCodeIdHash
from qaseio.apis.paths.run_code import RunCode
from qaseio.apis.paths.run_code_id import RunCodeId
from qaseio.apis.paths.run_code_id_public import RunCodeIdPublic
from qaseio.apis.paths.run_code_id_complete import RunCodeIdComplete
from qaseio.apis.paths.search import Search
from qaseio.apis.paths.shared_step_code import SharedStepCode
from qaseio.apis.paths.shared_step_code_hash import SharedStepCodeHash
from qaseio.apis.paths.suite_code import SuiteCode
from qaseio.apis.paths.suite_code_id import SuiteCodeId

PathToApi = typing_extensions.TypedDict(
    'PathToApi',
    {
        PathValues.ATTACHMENT: Attachment,
        PathValues.ATTACHMENT_CODE: AttachmentCode,
        PathValues.ATTACHMENT_HASH: AttachmentHash,
        PathValues.AUTHOR: Author,
        PathValues.AUTHOR_ID: AuthorId,
        PathValues.CASE_CODE: CaseCode,
        PathValues.CASE_CODE_ID: CaseCodeId,
        PathValues.CUSTOM_FIELD: CustomField,
        PathValues.CUSTOM_FIELD_ID: CustomFieldId,
        PathValues.DEFECT_CODE: DefectCode,
        PathValues.DEFECT_CODE_ID: DefectCodeId,
        PathValues.DEFECT_CODE_RESOLVE_ID: DefectCodeResolveId,
        PathValues.DEFECT_CODE_STATUS_ID: DefectCodeStatusId,
        PathValues.ENVIRONMENT_CODE: EnvironmentCode,
        PathValues.ENVIRONMENT_CODE_ID: EnvironmentCodeId,
        PathValues.MILESTONE_CODE: MilestoneCode,
        PathValues.MILESTONE_CODE_ID: MilestoneCodeId,
        PathValues.PLAN_CODE: PlanCode,
        PathValues.PLAN_CODE_ID: PlanCodeId,
        PathValues.PROJECT: Project,
        PathValues.PROJECT_CODE: ProjectCode,
        PathValues.PROJECT_CODE_ACCESS: ProjectCodeAccess,
        PathValues.RESULT_CODE: ResultCode,
        PathValues.RESULT_CODE_ID: ResultCodeId,
        PathValues.RESULT_CODE_HASH: ResultCodeHash,
        PathValues.RESULT_CODE_ID_BULK: ResultCodeIdBulk,
        PathValues.RESULT_CODE_ID_HASH: ResultCodeIdHash,
        PathValues.RUN_CODE: RunCode,
        PathValues.RUN_CODE_ID: RunCodeId,
        PathValues.RUN_CODE_ID_PUBLIC: RunCodeIdPublic,
        PathValues.RUN_CODE_ID_COMPLETE: RunCodeIdComplete,
        PathValues.SEARCH: Search,
        PathValues.SHARED_STEP_CODE: SharedStepCode,
        PathValues.SHARED_STEP_CODE_HASH: SharedStepCodeHash,
        PathValues.SUITE_CODE: SuiteCode,
        PathValues.SUITE_CODE_ID: SuiteCodeId,
    }
)

path_to_api = PathToApi(
    {
        PathValues.ATTACHMENT: Attachment,
        PathValues.ATTACHMENT_CODE: AttachmentCode,
        PathValues.ATTACHMENT_HASH: AttachmentHash,
        PathValues.AUTHOR: Author,
        PathValues.AUTHOR_ID: AuthorId,
        PathValues.CASE_CODE: CaseCode,
        PathValues.CASE_CODE_ID: CaseCodeId,
        PathValues.CUSTOM_FIELD: CustomField,
        PathValues.CUSTOM_FIELD_ID: CustomFieldId,
        PathValues.DEFECT_CODE: DefectCode,
        PathValues.DEFECT_CODE_ID: DefectCodeId,
        PathValues.DEFECT_CODE_RESOLVE_ID: DefectCodeResolveId,
        PathValues.DEFECT_CODE_STATUS_ID: DefectCodeStatusId,
        PathValues.ENVIRONMENT_CODE: EnvironmentCode,
        PathValues.ENVIRONMENT_CODE_ID: EnvironmentCodeId,
        PathValues.MILESTONE_CODE: MilestoneCode,
        PathValues.MILESTONE_CODE_ID: MilestoneCodeId,
        PathValues.PLAN_CODE: PlanCode,
        PathValues.PLAN_CODE_ID: PlanCodeId,
        PathValues.PROJECT: Project,
        PathValues.PROJECT_CODE: ProjectCode,
        PathValues.PROJECT_CODE_ACCESS: ProjectCodeAccess,
        PathValues.RESULT_CODE: ResultCode,
        PathValues.RESULT_CODE_ID: ResultCodeId,
        PathValues.RESULT_CODE_HASH: ResultCodeHash,
        PathValues.RESULT_CODE_ID_BULK: ResultCodeIdBulk,
        PathValues.RESULT_CODE_ID_HASH: ResultCodeIdHash,
        PathValues.RUN_CODE: RunCode,
        PathValues.RUN_CODE_ID: RunCodeId,
        PathValues.RUN_CODE_ID_PUBLIC: RunCodeIdPublic,
        PathValues.RUN_CODE_ID_COMPLETE: RunCodeIdComplete,
        PathValues.SEARCH: Search,
        PathValues.SHARED_STEP_CODE: SharedStepCode,
        PathValues.SHARED_STEP_CODE_HASH: SharedStepCodeHash,
        PathValues.SUITE_CODE: SuiteCode,
        PathValues.SUITE_CODE_ID: SuiteCodeId,
    }
)
