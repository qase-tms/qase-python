# [Qase TestOps](https://qase.io) Tavern Reporter

[![PyPI version](https://img.shields.io/pypi/v/qase-tavern?style=flat-square)](https://pypi.org/project/qase-tavern/)
[![PyPI downloads](https://img.shields.io/pypi/dm/qase-tavern?style=flat-square)](https://pypi.org/project/qase-tavern/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg?style=flat-square)](https://www.apache.org/licenses/LICENSE-2.0)

Qase Tavern Reporter enables seamless integration between your Tavern API tests and [Qase TestOps](https://qase.io), providing automatic test result reporting, test case management, and comprehensive test analytics.

## Features

- Link automated tests to Qase test cases by ID
- Auto-create test cases from your test files
- Report test results with test stages as steps
- Multi-project reporting support
- Flexible configuration (file, environment variables, CLI)

## Installation

```sh
pip install qase-tavern
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

```yaml
---
test_name: QaseID=1 Get user by ID

stages:
  - name: Get user
    request:
      url: https://api.example.com/users/1
      method: GET
    response:
      status_code: 200
```

**3. Run your tests:**

```sh
pytest
```

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
      "title": "Tavern API Tests"
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

Associate your tests with Qase test cases by adding `QaseID={ID}` to the test name:

```yaml
---
test_name: QaseID=1 Get user profile

stages:
  - name: Get user profile
    request:
      url: https://api.example.com/profile
      method: GET
    response:
      status_code: 200
      json:
        id: 1
        name: "John Doe"
```

### Multiple Qase IDs

Link one test to multiple test cases:

```yaml
---
test_name: QaseID=1,2,3 User authentication flow

stages:
  - name: Login
    request:
      url: https://api.example.com/auth/login
      method: POST
      json:
        username: testuser
        password: testpass
    response:
      status_code: 200
```

### Test Result Statuses

| Tavern Result | Qase Status |
|---------------|-------------|
| Passed | `passed` |
| Failed (assertion) | `failed` |
| Failed (other) | `invalid` |
| Skipped | `skipped` |

### Stages as Steps

Each Tavern stage is automatically reported as a test step in Qase:

```yaml
---
test_name: QaseID=1 Complete order flow

stages:
  - name: Add item to cart          # Step 1
    request:
      url: https://api.example.com/cart
      method: POST
    response:
      status_code: 201

  - name: Proceed to checkout       # Step 2
    request:
      url: https://api.example.com/checkout
      method: POST
    response:
      status_code: 200

  - name: Complete payment          # Step 3
    request:
      url: https://api.example.com/payment
      method: POST
    response:
      status_code: 200
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

### Run Specific Test File

```sh
pytest test_api.tavern.yaml
```

## Requirements

- Python >= 3.9
- tavern >= 2.11.0

## Documentation

| Guide | Description |
|-------|-------------|
| [Usage Guide](docs/usage.md) | Complete usage reference with all options |
| [Multi-Project Support](docs/MULTI_PROJECT.md) | Reporting to multiple Qase projects |

## Examples

See the [examples directory](../examples/) for complete working examples.

## License

Apache License 2.0. See [LICENSE](../LICENSE) for details.
