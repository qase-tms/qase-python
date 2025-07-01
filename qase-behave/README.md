# [Qase TestOps](https://qase.io) Behave Reporter

[![License](https://lxgaming.github.io/badges/License-Apache%202.0-blue.svg)](https://www.apache.org/licenses/LICENSE-2.0)

## Installation

To install the latest version, run:

```sh
pip install qase-behave
```

## Getting started

The Behave reporter can auto-generate test cases
and suites from your test data.
Test results of subsequent test runs will match the same test cases
as long as their names and file paths don't change.

You can also annotate the tests with the IDs of existing test cases
from Qase.io before executing tests. It's a more reliable way to bind
autotests to test cases, that persists when you rename, move, or
parameterize your tests.

### Metadata

- `qase.id` - set the ID of the test case
- `qase.fields` - set the fields of the test case
- `qase.suite` - set the suite of the test case
- `qase.ignore` - ignore the test case in Qase. The test will be executed, but the results will not be sent to Qase.

For detailed instructions on using annotations and methods, refer to [Usage](docs/usage.md).

For information about attaching files and content or adding comments to test results, see [Attachments](docs/ATTACHMENTS.md).

For example:

```gherkin
Feature: Example tests

  @qase.id:1 @qase.fields:{"description":"It_is_simple_test"} @qase.suite:MySuite
  Scenario: Example test
    Given I have a simple test
    When I run it
    Then it should pass
```

To execute Behave tests and report them to Qase.io, run the command:

```bash
behave --format=qase.behave.formatter:QaseFormatter
```

You can try it with the example project at [`examples/behave`](../examples/behave/).

## Configuration

Qase Behave Reporter is configured in multiple ways:

- using a config file `qase.config.json`
- using environment variables
- using command line options

Environment variables override the values given in the config file,
and command line options override both other values.

Configuration options are described in the
[configuration reference](docs/CONFIGURATION.md).

### Example: qase.config.json

```json
{
  "mode": "testops",
  "fallback": "report",
  "testops": {
    "project": "YOUR_PROJECT_CODE",
    "api": {
      "token": "YOUR_API_TOKEN",
      "host": "qase.io"
    },
    "run": {
      "title": "Test run title"
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
  "environment": "local"
}
```

## Requirements

We maintain the reporter on [LTS versions of Python](https://devguide.python.org/versions/).

`python >= 3.7`
`behave >= 1.2.6`

<!-- references -->

