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
from qaseio import QaseApi

qase = QaseApi("api_token")
```

### Projects ###

#### Get All Projects ####
This method allows to retrieve all projects available for your account. You can you limit and offset params to paginate.

```python
projects = qase.projects.get_all()
```

#### Get All Projects ####
This method allows to retrieve a specific project.

```python
project = qase.projects.get("PRJCODE")
```

#### Create a new project ####
This method is used to create a new project through API.

```python
from qaseio.models import ProjectCreate

project = qase.projects.create(
    ProjectCreate("Test project", "PRJCODE")
)
```

### Test cases ###

#### Get all test cases ####
This method allows to retrieve all test cases stored in selected project. You can you limit and offset params to paginate.

```python
test_cases = qase.test_cases.get_all("PRJCODE")
```

#### Get a specific test case ####
This method allows to retrieve a specific test case.

```python
test_case = qase.test_cases.get("PRJCODE", 4)
```

#### Delete test case ####
This method completely deletes a test case from repository.

```python
qase.test_cases.delete("PRJCODE", 4)
```

### Test runs ###

#### Get all test runs ####
This method allows to retrieve all test runs stored in selected project. You can you limit and offset params to paginate.

```python
from qaseio.models import TestRunInclude
test_runs = qase.runs.get_all("PRJCODE", include=TestRunInclude.CASES)
```

#### Get a specific test run ####
This method allows to retrieve a specific test run.

```python
test_run = qase.runs.get("PRJCODE", 4)
```

#### Create a new test run ####
This method is used to create a new test run through API.

```python
from qaseio.models import TestRunCreate

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
from qaseio.models import TestRunResultCreate, TestRunResultStatus

test_run_result = qase.results.create(
    "PRJCODE",
    4,
    TestRunResultCreate(123, TestRunResultStatus.PASSED),
)
```

#### Update test run result ####
This method is used to update existing test run result through API.

```python
from qaseio.models import TestRunResultUpdate, TestRunResultStatus

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
