# [Qase TMS](https://qase.io) Robot Framework Listener

[![License](https://lxgaming.github.io/badges/License-Apache%202.0-blue.svg)](https://www.apache.org/licenses/LICENSE-2.0)

## Installation

```
pip install qase-robotframework
```

## Usage

You must add Qase case IDs to robot framework tests.
They should be added as a tags in form like `Q-<case id without project code>`. Examples:

```robotframework
*** Test Cases ***
Push button
    [Tags]  Q-2
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

After adding new tags and configuring listener - you could simply use it like this:

```
robot --listener qaseio.robotframework.Listener keyword_driven.robot data_driven.robot
```

## Configuration

Listener supports loading configuration both from environment variables and from `tox.ini` file.

ENV variables:
- `QASE_API_TOKEN` - API token to access Qase TMS
- `QASE_PROJECT` - Project code from Qase TMS
- `QASE_RUN_ID` - Run ID if you want to add results to existing run
- `QASE_RUN_NAME` - Set custom run name when no run ID is provided

`tox.ini` configuration:

```ini
[qase]
qase_api_token=<API TOKEN>
qase_project=PROJECTCODE
qase_run_id=14
qase_run_name=New Robot Framework Run
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
