# [Qase TMS](https://qase.io) Pytest Plugin

[![License](https://lxgaming.github.io/badges/License-Apache%202.0-blue.svg)](https://www.apache.org/licenses/LICENSE-2.0)

# Installation

```
pip install qase-pytest
```

# Usage

## Configuration

Configuration could be provided both by `pytest.ini`/`tox.ini` params
and using command-line arguments:

* Command-line args:
```
  --qase                Use Qase TMS
  --qase-api-token=QS_API_TOKEN
                        Api token for Qase TMS
  --qase-project=QS_PROJECT_CODE
                        Project code in Qase TMS
  --qase-testrun=QS_TESTRUN_ID
                        Testrun ID in Qase TMS
  --qase-debug=QS_DEBUG
                        Prints additional output of plugin
```

* INI file parameters:

```
  qs_enabled (bool):    default value for --qase
  qs_api_token (string):
                        default value for --qase-api-token
  qs_project_code (string):
                        default value for --qase-project
  qs_testrun_id (string):
                        default value for --qase-testrun
  qs_debug (bool):      default value for --qase-debug
```

## Link tests with test-cases

To link tests with test-cases in Qase TMS you should use predefined decorator:

```python
from qaseio.pytest import qase

@qase.id(13)
def test_example_1():
    pass

@qase.id(12, 156)
def test_example_2():
    pass
```

You could pass as much IDs as you need.

## Execution logic

1. Check project exists
2. Check testrun exists
3. Load all ids for each test-case
4. Check which tests does not have ids (debug: will list them all)
5. Check every id exists in project (debug: will show which missing)
6. Check every id present in testrun (debug: will show which missing)
7. Execute tests and publish results in a runtime,
not waiting all run to finish
