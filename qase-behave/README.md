# [Qase TestOps](https://qase.io) Behave Reporter

[![PyPI version](https://img.shields.io/pypi/v/qase-behave?style=flat-square)](https://pypi.org/project/qase-behave/)
[![PyPI downloads](https://img.shields.io/pypi/dm/qase-behave?style=flat-square)](https://pypi.org/project/qase-behave/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg?style=flat-square)](https://www.apache.org/licenses/LICENSE-2.0)

Qase Behave Reporter enables seamless integration between your Behave BDD tests and [Qase TestOps](https://qase.io), providing automatic test result reporting, test case management, and comprehensive test analytics.

## Features

- Link automated tests to Qase test cases by ID
- Auto-create test cases from your feature files
- Report test results with rich metadata (fields, attachments)
- Automatic step reporting from Gherkin scenarios
- Multi-project reporting support
- Flexible configuration (file, environment variables)

## Installation

```sh
pip install qase-behave
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

**2. Add Qase ID to your scenario:**

```gherkin
Feature: Authentication

  @qase.id:1
  Scenario: User can log in with valid credentials
    Given I am on the login page
    When I enter valid credentials
    Then I should see the dashboard
```

**3. Run your tests:**

```sh
behave --format=qase.behave.formatter:QaseFormatter
```

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
      "title": "Behave Automated Run"
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

Associate your scenarios with Qase test cases using the `@qase.id` tag:

```gherkin
Feature: Shopping Cart

  @qase.id:1
  Scenario: Add item to cart
    Given I am on the product page
    When I click add to cart
    Then the item should be in my cart

  @qase.id:2
  Scenario: Remove item from cart
    Given I have an item in my cart
    When I click remove
    Then my cart should be empty
```

### Add Metadata

Enhance your scenarios with additional information using the `@qase.fields` tag:

```gherkin
Feature: Checkout

  @qase.id:1
  @qase.fields:{"severity":"critical","priority":"high","layer":"e2e"}
  @qase.suite:Checkout
  Scenario: Complete purchase
    Given I have items in my cart
    When I complete checkout
    Then I should see order confirmation
```

**Note:** In field values, use underscores (`_`) instead of spaces. They will be automatically converted.

### Ignore Tests

Exclude specific scenarios from Qase reporting:

```gherkin
Feature: Authentication

  @qase.ignore
  Scenario: Work in progress test
    Given this test is not ready
    Then it should not be reported
```

### Test Result Statuses

| Behave Result | Qase Status |
|---------------|-------------|
| Passed | `passed` |
| Failed (AssertionError) | `failed` |
| Failed (other exception) | `invalid` |
| Skipped | `skipped` |

### Attachments

Attach files and content to test results in step definitions:

```python
from behave import given, when, then
from qase.behave import qase

@when('I take a screenshot')
def step_impl(context):
    screenshot = context.browser.get_screenshot_as_png()
    qase.attach(content=screenshot, file_name="screenshot.png", mime_type="image/png")
```

> For detailed usage examples, see the [Usage Guide](docs/usage.md).

## Running Tests

### Basic Execution

```sh
behave --format=qase.behave.formatter:QaseFormatter
```

### With Environment Variables

```sh
export QASE_MODE=testops
export QASE_TESTOPS_PROJECT=PROJ
export QASE_TESTOPS_API_TOKEN=your_token
behave --format=qase.behave.formatter:QaseFormatter
```

### With Custom Run Title

```sh
export QASE_TESTOPS_RUN_TITLE="Regression Run"
behave --format=qase.behave.formatter:QaseFormatter
```

## Requirements

- Python >= 3.9
- behave >= 1.2.6

## Documentation

| Guide | Description |
|-------|-------------|
| [Usage Guide](docs/usage.md) | Complete usage reference with all tags and options |
| [Attachments](docs/ATTACHMENTS.md) | Adding screenshots, logs, and files to test results |
| [Multi-Project Support](docs/MULTI_PROJECT.md) | Reporting to multiple Qase projects |

## Examples

See the [examples directory](../examples/single/behave/) for complete working examples.

## License

Apache License 2.0. See [LICENSE](../LICENSE) for details.
