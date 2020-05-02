# [Qase TMS](https://qase.io) Python Api Client

[![License](https://lxgaming.github.io/badges/License-Apache%202.0-blue.svg)](https://www.apache.org/licenses/LICENSE-2.0)

# Installation

TBD

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
    TestRunCreate("Test run", [1, 2, 3])
)
```

#### Delete test run ####
This method completely deletes a test run from repository.

```python
qase.runs.delete("PRJCODE", 4)
```
