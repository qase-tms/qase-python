# flake8: noqa

if __import__("typing").TYPE_CHECKING:
    # import apis into api package
    from qase.api_client_v1.api.attachments_api import AttachmentsApi
    from qase.api_client_v1.api.authors_api import AuthorsApi
    from qase.api_client_v1.api.cases_api import CasesApi
    from qase.api_client_v1.api.configurations_api import ConfigurationsApi
    from qase.api_client_v1.api.custom_fields_api import CustomFieldsApi
    from qase.api_client_v1.api.defects_api import DefectsApi
    from qase.api_client_v1.api.environments_api import EnvironmentsApi
    from qase.api_client_v1.api.milestones_api import MilestonesApi
    from qase.api_client_v1.api.plans_api import PlansApi
    from qase.api_client_v1.api.projects_api import ProjectsApi
    from qase.api_client_v1.api.results_api import ResultsApi
    from qase.api_client_v1.api.runs_api import RunsApi
    from qase.api_client_v1.api.search_api import SearchApi
    from qase.api_client_v1.api.shared_parameters_api import SharedParametersApi
    from qase.api_client_v1.api.shared_steps_api import SharedStepsApi
    from qase.api_client_v1.api.suites_api import SuitesApi
    from qase.api_client_v1.api.system_fields_api import SystemFieldsApi
    from qase.api_client_v1.api.users_api import UsersApi
    
else:
    from lazy_imports import LazyModule, as_package, load

    load(
        LazyModule(
            *as_package(__file__),
            """# import apis into api package
from qase.api_client_v1.api.attachments_api import AttachmentsApi
from qase.api_client_v1.api.authors_api import AuthorsApi
from qase.api_client_v1.api.cases_api import CasesApi
from qase.api_client_v1.api.configurations_api import ConfigurationsApi
from qase.api_client_v1.api.custom_fields_api import CustomFieldsApi
from qase.api_client_v1.api.defects_api import DefectsApi
from qase.api_client_v1.api.environments_api import EnvironmentsApi
from qase.api_client_v1.api.milestones_api import MilestonesApi
from qase.api_client_v1.api.plans_api import PlansApi
from qase.api_client_v1.api.projects_api import ProjectsApi
from qase.api_client_v1.api.results_api import ResultsApi
from qase.api_client_v1.api.runs_api import RunsApi
from qase.api_client_v1.api.search_api import SearchApi
from qase.api_client_v1.api.shared_parameters_api import SharedParametersApi
from qase.api_client_v1.api.shared_steps_api import SharedStepsApi
from qase.api_client_v1.api.suites_api import SuitesApi
from qase.api_client_v1.api.system_fields_api import SystemFieldsApi
from qase.api_client_v1.api.users_api import UsersApi

""",
            name=__name__,
            doc=__doc__,
        )
    )
