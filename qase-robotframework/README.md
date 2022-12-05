> # Qase Robot Framework Listener
>
> Publish results simple and easy.

## How to integrate

```
pip install qase-robotframework
```

## Usage

If you want to create a persistent link to Test Cases in Qase, you should add Qase test case IDs to robot framework tests.
They should be added as a tags in form like `Q-<case id without project code>`. You can use upper and lower case to indicate the test case IDs. Example:

```robotframework
*** Test Cases ***
Push button
    [Tags]  q-2
    Push button    1
    Result should be    1

Push multiple buttons
    [Tags]  Q-3
    Push button    1
    Push button    2
    Result should be    12
```

```robotframework
*** Test Cases ***    Expression    Expected
Addition              12 + 2 + 2    16
                      2 + -3        -1
    [Tags]   Q-7

Subtraction           12 - 2 - 2    8
                      2 - -3        5
    [Tags]   Q-8
```

### Working with steps

Listener supports reporting steps results:

Example:
```robotframework
Quick Get A JSON Body Test                                                  ## Test case: "Quick Get A JSON Body Test"
    [Tags]  Q-3
    ${response}=    GET  https://jsonplaceholder.typicode.com/posts/1       ## 1-st step - "GET"
    Should Be Equal As Strings    1  ${response.json()}[id]                 ## 2-nd step - "Should Be Equal As Strings"

Initializing the test case                                                  ## Test case: "Initializing the test case"
    [Tags]  q-4
    Set To Dictionary    ${info}   field1=A sample string                   ## 1-st step - "Set To Dictionary"
```

## Configuration

Listener supports loading configuration both from environment variables and from `tox.ini` file.

ENV variables:
- `QASE_MODE` - Define mode: `testops` to enable report
- `QASE_ENVIRONMENT` - Environment ID for the run
- `QASE_DEBUG` - If passed something - will enable debug logging for listener. Default: `False`
- `QASE_TESTOPS_MODE` - You can switch between `sync` and `async` modes. Default is `async`
- `QASE_TESTOPS_API_TOKEN` - API token to access Qase TestOps
- `QASE_TESTOPS_PROJECT` - Project code from Qase TestOps
- `QASE_TESTOPS_PLAN_ID` - Plan ID if you want to add results to existing run from Test Plan
- `QASE_TESTOPS_RUN_ID` - Run ID if you want to add results to existing run
- `QASE_TESTOPS_RUN_TITLE` - Set custom run name when no run ID is provided
- `QASE_TESTOPS_COMPLETE_RUN` - Will complete run after all tests are finished. Default: `False`
- `QASE_TESTOPS_HOST` - Define a host for Qase TestOps. Default: `qase.io`
### Usage:
```
QASE_API_TOKEN=<API TOKEN> QASE_PROJECT=PRJCODE robot --listener qaseio.robotframework.QaseListener keyword_driven.robot data_driven.robot
```
Moving variables to `tox.ini`, example configuration:
```ini
[qase]
qase_testops_api_token=api_key
qase_testops_project=project_code
qase_testops_run_id=run_id
qase_testops_run_title=New Robot Framework Run
qase_debug=True
qase_testops_complete_run=True
```
Execution:
```
robot --listener qaseio.robotframework.Listener someTest.robot
```
## Contribution

Install project locally:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .[testing]
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
