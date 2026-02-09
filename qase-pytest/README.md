# [Qase TestOps](https://qase.io) Pytest Reporter

[![PyPI version](https://img.shields.io/pypi/v/qase-pytest?style=flat-square)](https://pypi.org/project/qase-pytest/)
[![PyPI downloads](https://img.shields.io/pypi/dm/qase-pytest?style=flat-square)](https://pypi.org/project/qase-pytest/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg?style=flat-square)](https://www.apache.org/licenses/LICENSE-2.0)

Qase Pytest Reporter enables seamless integration between your Pytest tests and [Qase TestOps](https://qase.io), providing automatic test result reporting, test case management, and comprehensive test analytics.

## Features

- Link automated tests to Qase test cases by ID
- Auto-create test cases from your test code
- Report test results with rich metadata (fields, attachments, steps)
- Support for parameterized tests
- Multi-project reporting support
- Flexible configuration (file, environment variables, CLI)
- Built-in support for Playwright-based tests

## Installation

```sh
pip install qase-pytest
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

```python
from qase.pytest import qase

@qase.id(1)
def test_example():
    assert True
```

**3. Run your tests:**

```sh
pytest
```

## Upgrading

For migration guides between major versions, see [Upgrade Guide](docs/UPGRADE.md).

## Configuration

The reporter is configured via (in order of priority):

1. **CLI options** (`--qase-*`, highest priority)
2. **Environment variables** (`QASE_*`)
3. **Config file** (`qase.config.json`)

### Minimal Configuration

| Option | Environment Variable | CLI Option | Description |
|--------|---------------------|------------|-------------|
| `mode` | `QASE_MODE` | `--qase-mode` | Set to `testops` to enable reporting |
| `testops.project` | `QASE_TESTOPS_PROJECT` | `--qase-testops-project` | Your Qase project code |
| `testops.api.token` | `QASE_TESTOPS_API_TOKEN` | `--qase-testops-api-token` | Your Qase API token |

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
      "title": "Pytest Automated Run"
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
  },
  "framework": {
    "pytest": {
      "captureLogs": true
    }
  }
}
```

> **Full configuration reference:** See [qase-python-commons](../qase-python-commons/README.md) for all available options including logging, status mapping, execution plans, and more.

## Usage

### Link Tests with Test Cases

Associate your tests with Qase test cases using test case IDs:

```python
from qase.pytest import qase

# Single ID
@qase.id(1)
def test_single_id():
    assert True

# Multiple IDs
@qase.id([2, 3])
def test_multiple_ids():
    assert True
```

### Add Metadata

Enhance your tests with additional information:

```python
from qase.pytest import qase

@qase.id(1)
@qase.title("User Login Test")
@qase.suite("Authentication")
@qase.fields(
    ("severity", "critical"),
    ("priority", "high"),
    ("layer", "e2e"),
    ("description", "Verify user can log in with valid credentials"),
    ("preconditions", "User account exists in the system"),
)
def test_user_login():
    assert True
```

### Ignore Tests

Exclude specific tests from Qase reporting (test still runs, but results are not sent):

```python
from qase.pytest import qase

@qase.ignore()
def test_not_reported():
    assert True
```

### Test Result Statuses

| Pytest Result | Qase Status |
|---------------|-------------|
| Passed | `passed` |
| Failed (AssertionError) | `failed` |
| Failed (other exception) | `invalid` |
| Skipped | `skipped` |

### Attachments

Attach files, screenshots, and logs to test results:

```python
from qase.pytest import qase

def test_with_attachments():
    # Attach file from path
    qase.attach("/path/to/file.txt")

    # Attach with custom MIME type
    qase.attach(("/path/to/file.json", "application/json"))

    # Attach content from memory
    qase.attach((b"screenshot data", "image/png", "screenshot.png"))

    assert True
```

### Test Steps

Define test steps for detailed reporting:

```python
from qase.pytest import qase

@qase.step("Open login page")
def open_login():
    pass

@qase.step("Enter credentials")
def enter_credentials(username, password):
    pass

def test_login():
    open_login()
    enter_credentials("user", "pass")

    # Inline step with context manager
    with qase.step("Click login button"):
        pass
```

> For detailed usage examples, see the [Usage Guide](docs/usage.md).

## Running Tests

### Basic Execution

```sh
pytest
```

### With CLI Options

```sh
pytest \
    --qase-mode=testops \
    --qase-testops-project=PROJ \
    --qase-testops-api-token=your_token
```

### With Environment Variables

```sh
export QASE_MODE=testops
export QASE_TESTOPS_PROJECT=PROJ
export QASE_TESTOPS_API_TOKEN=your_token
pytest
```

### With Existing Test Run

```sh
pytest --qase-testops-run-id=123
```

### With Test Plan

```sh
pytest --qase-testops-plan-id=456
```

## Requirements

- Python >= 3.9
- pytest >= 7.0.0

## Documentation

| Guide | Description |
|-------|-------------|
| [Usage Guide](docs/usage.md) | Complete usage reference with all decorators and options |
| [Attachments](docs/ATTACHMENTS.md) | Adding screenshots, logs, and files to test results |
| [Steps](docs/STEPS.md) | Defining test steps for detailed reporting |
| [Parameters](docs/PARAMETERS.md) | Working with parameterized tests |
| [Multi-Project Support](docs/MULTI_PROJECT.md) | Reporting to multiple Qase projects |
| [Upgrade Guide](docs/UPGRADE.md) | Migration guide for breaking changes |

## Examples

See the [examples directory](../examples/) for complete working examples.

## License

Apache License 2.0. See [LICENSE](../LICENSE) for details.
