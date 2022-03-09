
# flake8: noqa

# Import all APIs into this package.
# If you have many APIs here with many many models used in each API this may
# raise a `RecursionError`.
# In order to avoid this, import only the API that you directly need like:
#
#   from .api.attachments_api import AttachmentsApi
#
# or import this package, but before doing it, use:
#
#   import sys
#   sys.setrecursionlimit(n)

# Import APIs into API package:
from qaseio.api.attachments_api import AttachmentsApi
from qaseio.api.cases_api import CasesApi
from qaseio.api.custom_fields_api import CustomFieldsApi
from qaseio.api.defects_api import DefectsApi
from qaseio.api.environments_api import EnvironmentsApi
from qaseio.api.milestones_api import MilestonesApi
from qaseio.api.plans_api import PlansApi
from qaseio.api.projects_api import ProjectsApi
from qaseio.api.results_api import ResultsApi
from qaseio.api.runs_api import RunsApi
from qaseio.api.search_api import SearchApi
from qaseio.api.shared_steps_api import SharedStepsApi
from qaseio.api.suites_api import SuitesApi
