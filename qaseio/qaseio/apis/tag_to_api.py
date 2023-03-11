import typing_extensions

from qaseio.apis.tags import TagValues
from qaseio.apis.tags.attachments_api import AttachmentsApi
from qaseio.apis.tags.authors_api import AuthorsApi
from qaseio.apis.tags.cases_api import CasesApi
from qaseio.apis.tags.custom_fields_api import CustomFieldsApi
from qaseio.apis.tags.environments_api import EnvironmentsApi
from qaseio.apis.tags.defects_api import DefectsApi
from qaseio.apis.tags.plans_api import PlansApi
from qaseio.apis.tags.projects_api import ProjectsApi
from qaseio.apis.tags.results_api import ResultsApi
from qaseio.apis.tags.milestones_api import MilestonesApi
from qaseio.apis.tags.runs_api import RunsApi
from qaseio.apis.tags.search_api import SearchApi
from qaseio.apis.tags.shared_steps_api import SharedStepsApi
from qaseio.apis.tags.suites_api import SuitesApi

TagToApi = typing_extensions.TypedDict(
    'TagToApi',
    {
        TagValues.ATTACHMENTS: AttachmentsApi,
        TagValues.AUTHORS: AuthorsApi,
        TagValues.CASES: CasesApi,
        TagValues.CUSTOMFIELDS: CustomFieldsApi,
        TagValues.ENVIRONMENTS: EnvironmentsApi,
        TagValues.DEFECTS: DefectsApi,
        TagValues.PLANS: PlansApi,
        TagValues.PROJECTS: ProjectsApi,
        TagValues.RESULTS: ResultsApi,
        TagValues.MILESTONES: MilestonesApi,
        TagValues.RUNS: RunsApi,
        TagValues.SEARCH: SearchApi,
        TagValues.SHAREDSTEPS: SharedStepsApi,
        TagValues.SUITES: SuitesApi,
    }
)

tag_to_api = TagToApi(
    {
        TagValues.ATTACHMENTS: AttachmentsApi,
        TagValues.AUTHORS: AuthorsApi,
        TagValues.CASES: CasesApi,
        TagValues.CUSTOMFIELDS: CustomFieldsApi,
        TagValues.ENVIRONMENTS: EnvironmentsApi,
        TagValues.DEFECTS: DefectsApi,
        TagValues.PLANS: PlansApi,
        TagValues.PROJECTS: ProjectsApi,
        TagValues.RESULTS: ResultsApi,
        TagValues.MILESTONES: MilestonesApi,
        TagValues.RUNS: RunsApi,
        TagValues.SEARCH: SearchApi,
        TagValues.SHAREDSTEPS: SharedStepsApi,
        TagValues.SUITES: SuitesApi,
    }
)
