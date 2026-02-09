# [Qase TestOps](https://qase.io) Robot Framework Reporter

[![PyPI version](https://img.shields.io/pypi/v/qase-robotframework?style=flat-square)](https://pypi.org/project/qase-robotframework/)
[![PyPI downloads](https://img.shields.io/pypi/dm/qase-robotframework?style=flat-square)](https://pypi.org/project/qase-robotframework/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg?style=flat-square)](https://www.apache.org/licenses/LICENSE-2.0)

Qase Robot Framework Reporter enables seamless integration between your Robot Framework tests and [Qase TestOps](https://qase.io), providing automatic test result reporting, test case management, and comprehensive test analytics.

## Features

- Link automated tests to Qase test cases by ID
- Auto-create test cases from your test suites
- Report test results with rich metadata (fields, parameters)
- Automatic step reporting from keywords
- Multi-project reporting support
- Support for parallel execution with pabot
- Flexible configuration (file, environment variables)

## Installation

```sh
pip install qase-robotframework
```

## Quick Start

**1. Create `qase.config.json` in your project root:**

```json
{
  "mode": "testops",
  "testops": {
    "project": "YOUR_PROJECT_CODE",
    "api": {
      "token": "YOUR_API_TOKEN"
    }
  }
}
```

**2. Add Qase ID to your test:**

```robotframework
*** Test Cases ***
User can log in with valid credentials
    [Tags]    Q-1
    Open Login Page
    Enter Valid Credentials
    Verify Dashboard Is Visible
```

**3. Run your tests:**

```sh
robot --listener qase.robotframework.Listener tests/
```

## Upgrading

For migration guides between major versions, see [Upgrade Guide](docs/UPGRADE.md).

## Configuration

The reporter is configured via (in order of priority):

1. **Environment variables** (`QASE_*`, highest priority)
2. **Config file** (`qase.config.json`)

### Minimal Configuration

| Option | Environment Variable | Description |
|--------|---------------------|-------------|
| `mode` | `QASE_MODE` | Set to `testops` to enable reporting |
| `testops.project` | `QASE_TESTOPS_PROJECT` | Your Qase project code |
| `testops.api.token` | `QASE_TESTOPS_API_TOKEN` | Your Qase API token |

### Example `qase.config.json`

```json
{
  "mode": "testops",
  "fallback": "report",
  "testops": {
    "project": "YOUR_PROJECT_CODE",
    "api": {
      "token": "YOUR_API_TOKEN"
    },
    "run": {
      "title": "Robot Framework Automated Run"
    },
    "batch": {
      "size": 100
    }
  },
  "report": {
    "driver": "local",
    "connection": {
      "local": {
        "path": "./build/qase-report",
        "format": "json"
      }
    }
  }
}
```

> **Full configuration reference:** See [qase-python-commons](../qase-python-commons/README.md) for all available options including logging, status mapping, execution plans, and more.

## Usage

### Link Tests with Test Cases

Associate your tests with Qase test cases using the `Q-{ID}` tag:

```robotframework
*** Test Cases ***
User Registration
    [Tags]    Q-1
    Open Registration Page
    Fill Registration Form
    Submit Form
    Verify Registration Success

User Login
    [Tags]    Q-2    Q-3
    Open Login Page
    Enter Credentials
    Click Login Button
```

### Add Metadata

Enhance your tests with fields using the `qase.fields` tag:

```robotframework
*** Test Cases ***
Critical Purchase Flow
    [Tags]    Q-1    qase.fields:{"severity":"critical","priority":"high","layer":"e2e"}
    [Documentation]    Verify user can complete a purchase
    Add Item To Cart
    Proceed To Checkout
    Complete Payment
```

### Add Parameters

Report specific variables as parameters using the `qase.params` tag:

```robotframework
*** Variables ***
${USERNAME}    testuser
${PASSWORD}    testpass

*** Test Cases ***
Login Test
    [Tags]    Q-1    qase.params:[USERNAME, PASSWORD]
    Login With Credentials    ${USERNAME}    ${PASSWORD}
    Verify Login Success
```

### Ignore Tests

Exclude specific tests from Qase reporting:

```robotframework
*** Test Cases ***
Work In Progress
    [Tags]    qase.ignore
    Log    This test is not reported to Qase
```

### Test Result Statuses

| Robot Framework Result | Qase Status |
|------------------------|-------------|
| PASS | `passed` |
| FAIL (AssertionError) | `failed` |
| FAIL (other exception) | `invalid` |
| SKIP | `skipped` |

> For detailed usage examples, see the [Usage Guide](docs/usage.md).

## Running Tests

### Basic Execution

```sh
robot --listener qase.robotframework.Listener tests/
```

### With Environment Variables

```sh
export QASE_MODE=testops
export QASE_TESTOPS_PROJECT=PROJ
export QASE_TESTOPS_API_TOKEN=your_token
robot --listener qase.robotframework.Listener tests/
```

### With Robot Variables

```sh
robot --listener qase.robotframework.Listener \
    --variable QASE_TESTOPS_PROJECT:PROJ \
    --variable QASE_TESTOPS_API_TOKEN:your_token \
    tests/
```

### Parallel Execution with Pabot

```sh
pabot --listener qase.robotframework.Listener tests/
```

## Requirements

- Python >= 3.9
- robotframework >= 5.0.0

## Documentation

| Guide | Description |
|-------|-------------|
| [Usage Guide](docs/usage.md) | Complete usage reference with all tags and options |
| [Multi-Project Support](docs/MULTI_PROJECT.md) | Reporting to multiple Qase projects |
| [Upgrade Guide](docs/UPGRADE.md) | Migration guide for breaking changes |

## Examples

See the [examples directory](../examples/) for complete working examples.

## License

Apache License 2.0. See [LICENSE](../LICENSE) for details.
