# [Qase TestOps](https://qase.io) Tavern Reporter

[![License](https://lxgaming.github.io/badges/License-Apache%202.0-blue.svg)](https://www.apache.org/licenses/LICENSE-2.0)

## Installation

To install the latest version, run:

```sh
pip install pre qase-tavern
```

## Getting started

The Tavern reporter can auto-generate test cases
and suites from your test data.
Test results of subsequent test runs will match the same test cases
as long as their names and file paths don't change.

You can also annotate the tests with the IDs of existing test cases
from Qase.io before executing tests. It's a more reliable way to bind
autotests to test cases, that persists when you rename, move, or
parameterize your tests.

For detailed instructions on using annotations and methods, refer to [Usage](docs/usage.md).

For example:

```yaml
---
test_name: QaseID=1 Test with QaseID success

stages:
  - name: Step 1
    request:
    response:

  - name: Step 2
    request:
    response:
```

To execute Tavern tests and report them to Qase.io, run the command:

```bash
pytest
```

You can try it with the example project at [`examples/tavern`](../examples/tavern/).

## Configuration

Qase Tavern Reporter is configured in multiple ways:

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
`tavern >= 2.11.0`

<!-- references -->

[auth]: https://developers.qase.io/#authentication
