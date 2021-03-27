# [Qase TMS](https://qase.io) Python Api Client

[![License](https://lxgaming.github.io/badges/License-Apache%202.0-blue.svg)](https://www.apache.org/licenses/LICENSE-2.0)

# Installation

```
pip install qaseio
```

## Usage ##
Qase.io uses API tokens to authenticate requests. You can view an manage your API keys in [API tokens pages](https://app.qase.io/user/api/token).

You must replace api_token with your personal API key.

```python
from qaseio.client import QaseApi

qase = QaseApi("api_token")
```

### Projects ###

#### Get All Projects ####
This method allows to retrieve all projects available for your account. You can you limit and offset params to paginate.

```python
projects = qase.projects.get_all()
```

#### Get a specific project ####
This method allows to retrieve a specific project.

```python
project = qase.projects.get("PRJCODE")
```

#### Check project exists ####

```python
exists = qase.projects.exists("PRJCODE")
```

#### Create a new project ####
This method is used to create a new project through API.

```python
from qaseio.client.models import ProjectCreate

project = qase.projects.create(
    ProjectCreate("Test project", "PRJCODE")
)
```

### Test cases ###

#### Get all test cases ####
This method allows to retrieve all test cases stored in selected project. You can you limit and offset params to paginate.

```python
test_cases = qase.cases.get_all("PRJCODE")
```

#### Get a specific test case ####
This method allows to retrieve a specific test case.

```python
test_case = qase.cases.get("PRJCODE", 4)
```

#### Check test case exists ####

```python
exists = qase.cases.exists("PRJCODE", 4)
```

#### Delete test case ####
This method completely deletes a test case from repository.

```python
qase.cases.delete("PRJCODE", 4)
```

### Test Suites ###

#### Get all test suites ####
This method allows to retrieve all test suites stored in selected project. You can you limit and offset params to paginate.

```python
from qaseio.client.models import TestSuiteFilters

test_suites = qase.suites.get_all(
    "PRJCODE", filters=TestSuiteFilters(search="query")
)
```

#### Get a specific test suite ####
This method allows to retrieve a specific test suite.

```python
test_suite = qase.suites.get("PRJCODE", 123)
```

#### Check test suite exists ####

```python
exists = qase.suites.exists("PRJCODE", 123)
```

#### Create a new test suite ####
This method is used to create a new test plan through API.

```python
from qaseio.client.models import TestSuiteCreate

test_suite = qase.suites.create(
    "PRJCODE",
    TestSuiteCreate("New test suite"),
)
```

#### Update test suite ####
This method is used to update existing test suite through API.

```python
from qaseio.client.models import TestSuiteUpdate

test_suite = qase.suites.update(
    "PRJCODE",
    123,
    TestSuiteUpdate("Updated suite"),
)
```

#### Delete test suite ####
This method completely deletes a test suite from repository.

```python
qase.suites.delete("PRJCODE", 123)
```

### Milestones ###

#### Get all milestones ####
This method allows to retrieve all milestones stored in selected project. You can you limit and offset params to paginate.

```python
from qaseio.client.models import MilestoneFilters

milestones = qase.milestones.get_all(
    "PRJCODE", filters=MilestoneFilters(search="query")
)
```

#### Get a specific milestone ####
This method allows to retrieve a specific milestone.

```python
milestone = qase.milestones.get("PRJCODE", 123)
```

#### Check milestone exists ####

```python
exists = qase.milestones.exists("PRJCODE", 123)
```

#### Create a new milestone ####
This method is used to create a new test plan through API.

```python
from qaseio.client.models import MilestoneCreate

milestone = qase.milestones.create(
    "PRJCODE",
    MilestoneCreate("New test suite"),
)
```

#### Update milestone ####
This method is used to update existing milestone through API.

```python
from qaseio.client.models import MilestoneUpdate

test_suite = qase.milestones.update(
    "PRJCODE",
    123,
    MilestoneUpdate("Updated suite"),
)
```

#### Delete milestone ####
This method completely deletes a milestone from repository.

```python
qase.milestones.delete("PRJCODE", 123)
```

### Shared steps ###

#### Get all shared steps ####
This method allows to retrieve all shared steps stored in selected project. You can you limit and offset params to paginate.

```python
from qaseio.client.models import SharedStepFilters

shared_steps = qase.shared_steps.get_all(
    "PRJCODE", filters=SharedStepFilters(search="query")
)
```

#### Get a specific shared step ####
This method allows to retrieve a specific shared step.

```python
shared_step = qase.shared_steps.get("PRJCODE", "hash")
```

#### Check shared step exists ####

```python
exists = qase.shared_steps.exists("PRJCODE", "hash")
```

#### Create a new shared step ####
This method is used to create a new shared step through API.

```python
from qaseio.client.models import SharedStepCreate

shared_step = qase.shared_steps.create(
    "PRJCODE",
    SharedStepCreate("New step", "action"),
)
```

#### Update shared step ####
This method is used to update existing shared step through API.

```python
from qaseio.client.models import SharedStepUpdate

shared_step = qase.shared_steps.update(
    "PRJCODE",
    "hash",
    SharedStepUpdate("Updated step"),
)
```

#### Delete shared step ####
This method completely deletes a shared step from repository.

```python
qase.shared_steps.delete("PRJCODE", "hash")
```

### Test plans ###

#### Get all test plans ####
This method allows to retrieve all test plans stored in selected project. You can you limit and offset params to paginate.

```python
test_plans = qase.plans.get_all("PRJCODE")
```

#### Get a specific test plan ####
This method allows to retrieve a specific test plan.

```python
test_plan = qase.plans.get("PRJCODE", 123)
```

#### Check test plan exists ####

```python
exists = qase.plans.exists("PRJCODE", 123)
```

#### Create a new test plan ####
This method is used to create a new test plan through API.

```python
from qaseio.client.models import TestPlanCreate

test_plan = qase.plans.create(
    "PRJCODE",
    TestPlanCreate("New test run", [1, 2, 3]),
)
```

#### Update test plan ####
This method is used to update existing test plan through API.

```python
from qaseio.client.models import TestPlanCreate

test_plan = qase.plans.update(
    "PRJCODE",
    123,
    TestPlanCreate("New test run", [1, 2, 3]),
)
```

#### Delete test plan ####
This method completely deletes a test plan from repository.

```python
qase.plans.delete("PRJCODE", 123)
```

### Test runs ###

#### Get all test runs ####
This method allows to retrieve all test runs stored in selected project. You can you limit and offset params to paginate.

```python
from qaseio.client.models import TestRunInclude
test_runs = qase.runs.get_all("PRJCODE", include=TestRunInclude.CASES)
```

#### Get a specific test run ####
This method allows to retrieve a specific test run.

```python
test_run = qase.runs.get("PRJCODE", 4)
```

#### Check test run exists ####

```python
exists = qase.runs.exists("PRJCODE", 4)
```

#### Create a new test run ####
This method is used to create a new test run through API.

```python
from qaseio.client.models import TestRunCreate

test_run = qase.runs.create(
    "PRJCODE",
    TestRunCreate("Test run", [1, 2, 3]),
)
```

#### Delete test run ####
This method completely deletes a test run from repository.

```python
qase.runs.delete("PRJCODE", 4)
```

### Test run results ###

#### Get all test run results ####
This method allows to retrieve all test run results stored in selected project. You can you limit and offset params to paginate.

```python
test_run_results = qase.results.get_all("PRJCODE")
```

#### Get a specific test run result ####
This method allows to retrieve a specific test run result.

```python
test_run_result = qase.results.get("PRJCODE", "2898ba7f3b4d857cec8bee4a852cdc85f8b33132")
```

#### Create a new test run result ####
This method is used to create a new test run result through API.

```python
from qaseio.client.models import TestRunResultCreate, TestRunResultStatus

test_run_result = qase.results.create(
    "PRJCODE",
    4,
    TestRunResultCreate(123, TestRunResultStatus.PASSED),
)
```

#### Update test run result ####
This method is used to update existing test run result through API.

```python
from qaseio.client.models import TestRunResultUpdate, TestRunResultStatus

test_run_result = qase.results.update(
    "PRJCODE",
    4,
    "2898ba7f3b4d857cec8bee4a852cdc85f8b33132",
    TestRunResultUpdate(TestRunResultStatus.PASSED),
)
```

#### Delete test run result ####
This method completely deletes a test run result from repository.

```python
qase.results.delete("PRJCODE", 4, "2898ba7f3b4d857cec8bee4a852cdc85f8b33132")
```

### Defects ###

#### Get all defects ####
This method allows to retrieve all defects stored in selected project. You can you limit and offset params to paginate.

```python
from qaseio.client.models import DefectStatus, DefectFilters
defects = qase.defects.get_all("PRJCODE", filter=DefectFilters(DefectStatus.OPEN))
```

#### Get a specific defect ####
This method allows to retrieve a specific defect.

```python
defect = qase.defects.get("PRJCODE", 4)
```

#### Check defect exists ####

```python
exists = qase.defects.exists("PRJCODE", 4)
```

#### Resolve defect ####
This method is used to resolve defect through API.

```python
defect = qase.defects.resolve("PRJCODE", 4)
```

#### Delete defect ####
This method completely deletes a defect from repository.

```python
qase.defects.delete("PRJCODE", 4)
```

### Custom fields ###

#### Get all custom fields ####
This method allows to retrieve all custom fields stored in selected project. You can you limit and offset params to paginate.

```python
custom_fields = qase.custom_fields.get_all("PRJCODE")
```

#### Get a specific custom field ####
This method allows to retrieve a specific custom field.

```python
custom_field = qase.custom_fields.get("PRJCODE", 123)
```

#### Check custom field exists ####

```python
exists = qase.custom_fields.get("PRJCODE", 123)
```

### Attachments ###

#### Get all attachments ####
This method allows to retrieve all attachments stored in team. You can you limit and offset params to paginate.

```python
attachments = qase.attachments.get_all()
```

#### Get a specific attachment ####
This method allows to retrieve a specific attachment.

```python
attachment = qase.attachments.get("<hash>")
```

#### Check attachment exists ####

```python
exists = qase.attachments.exists("<hash>")
```

#### Upload new attachments ####
This method is used to upload new attachments through API. It supports different
input formats

```python
from qaseio.client.models import MimeTypes
results = qase.attachments.upload(
    "PRJCODE",
    "/absolute/path/to/file", # Upload file from absolute path
    "./relative/path/to/file", # Upload file from relative path
    # Upload file from path and specify mime-type
    ("./path/to/file", MimeTypes.CSV),
    # Upload bytes with given mime-type and filename
    (b"some bytes data", MimeTypes.JSON, "filename.json"),
)
```

You can specify as much files to upload as you need, according to API
[limits](https://developers.qase.io/#upload-attachmeent).

#### Delete attachment ####
This method completely deletes a attachment from repository.

```python
qase.attachments.delete("<hash>")
```

### Team ###

#### Get all team members ####
This method allows to retrieve all users in your team. You can you limit and offset params to paginate.

```python
users = qase.users.get_all()
```

#### Get a specific team member ####
This method allows to retrieve a specific user in your team.

```python
user = qase.users.get(123)
```

#### Check user exists ####

```python
exists = qase.users.get(123)
```

# Contribution

Install project locally:

```bash
python3 -m venv .venv
source .venv/bin/activate
python setup.py develop
```

Install dev requirements:

```bash
pip install pre-commit
pre-commit install
```

Test project:

```bash
tox
```
