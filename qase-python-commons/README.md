# Qase Python Commons

[![PyPI version](https://img.shields.io/pypi/v/qase-python-commons?style=flat-square)](https://pypi.org/project/qase-python-commons/)
[![PyPI downloads](https://img.shields.io/pypi/dm/qase-python-commons?style=flat-square)](https://pypi.org/project/qase-python-commons/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg?style=flat-square)](https://www.apache.org/licenses/LICENSE-2.0)

Core library for all Qase Python reporters. Contains the complete configuration reference.

## Table of Contents

- [About](#about)
- [Installation](#installation)
- [Reporters](#reporters)
- [Configuration](#configuration)
  - [Configuration Priority](#configuration-priority)
  - [Reporter Modes](#reporter-modes)
  - [Common Options](#common-options)
  - [TestOps Options (Single Project)](#testops-options-single-project)
  - [TestOps Multi Options (Multiple Projects)](#testops-multi-options-multiple-projects)
  - [Local Report Options](#local-report-options)
  - [Logging Options](#logging-options)
  - [Framework-Specific Options](#framework-specific-options)
- [Configuration Examples](#configuration-examples)
  - [Single Project (testops)](#single-project-testops)
  - [Multiple Projects (testops_multi)](#multiple-projects-testops_multi)
  - [Environment Variables](#environment-variables)
- [Profilers](#profilers)
- [Additional Features](#additional-features)
  - [Status Mapping](#status-mapping)
  - [Status Filtering](#status-filtering)
  - [External Links](#external-links)
  - [Test Run Configurations](#test-run-configurations)

---

## About

This module is an SDK for developing test reporters for Qase TMS. It uses `qase-api-client` as an API client, and all Qase Python reporters depend on this package.

**Use this library if:**
- You're developing a custom reporter for a specialized framework
- You need a complete configuration reference

**For testing, use the ready-made reporters** — see [Reporters](#reporters) section.

## Installation

```bash
pip install qase-python-commons
```

## Reporters

For popular frameworks, use the ready-made reporters:

| Framework | Package | Documentation |
|-----------|---------|---------------|
| Pytest | `qase-pytest` | [README](https://github.com/qase-tms/qase-python/tree/main/qase-pytest#readme) |
| Behave | `qase-behave` | [README](https://github.com/qase-tms/qase-python/tree/main/qase-behave#readme) |
| Robot Framework | `qase-robotframework` | [README](https://github.com/qase-tms/qase-python/tree/main/qase-robotframework#readme) |
| Tavern | `qase-tavern` | [README](https://github.com/qase-tms/qase-python/tree/main/qase-tavern#readme) |

---

## Configuration

### Configuration Priority

Qase Python reporters support three configuration methods (in order of priority):

1. **CLI options** (pytest and tavern only) — highest priority
2. **Environment variables** (`QASE_*`)
3. **Config file** (`qase.config.json`) — lowest priority

### Reporter Modes

The reporter mode is set via the `mode` option:

| Mode | Description |
|------|-------------|
| `testops` | Send results to a single Qase project |
| `testops_multi` | Send results to multiple projects |
| `report` | Generate a local JSON report |
| `off` | Reporter disabled (default) |

### Common Options

| Description | Config file | Environment variable | Default | Required |
|-------------|-------------|---------------------|---------|----------|
| Reporter mode | `mode` | `QASE_MODE` | `off` | No |
| Fallback mode | `fallback` | `QASE_FALLBACK` | `off` | No |
| Environment | `environment` | `QASE_ENVIRONMENT` | — | No |
| Root suite | `rootSuite` | `QASE_ROOT_SUITE` | — | No |
| Debug mode | `debug` | `QASE_DEBUG` | `False` | No |
| Execution plan path | `executionPlan.path` | `QASE_EXECUTION_PLAN_PATH` | `./build/qase-execution-plan.json` | No |
| Exclude parameters | `excludeParams` | `QASE_EXCLUDE_PARAMS` | — | No |
| Status mapping | `statusMapping` | `QASE_STATUS_MAPPING` | — | No |

### TestOps Options (Single Project)

| Description | Config file | Environment variable | Default | Required |
|-------------|-------------|---------------------|---------|----------|
| API token | `testops.api.token` | `QASE_TESTOPS_API_TOKEN` | — | Yes* |
| API host | `testops.api.host` | `QASE_TESTOPS_API_HOST` | `qase.io` | No |
| Project code | `testops.project` | `QASE_TESTOPS_PROJECT` | — | Yes* |
| Test run ID | `testops.run.id` | `QASE_TESTOPS_RUN_ID` | — | No |
| Test run title | `testops.run.title` | `QASE_TESTOPS_RUN_TITLE` | `Automated run <date>` | No |
| Test run description | `testops.run.description` | `QASE_TESTOPS_RUN_DESCRIPTION` | `<Framework> automated run` | No |
| Complete test run | `testops.run.complete` | `QASE_TESTOPS_RUN_COMPLETE` | `True` | No |
| Test run tags | `testops.run.tags` | `QASE_TESTOPS_RUN_TAGS` | `[]` | No |
| External link | `testops.run.externalLink` | `QASE_TESTOPS_RUN_EXTERNAL_LINK` | — | No |
| Test plan ID | `testops.plan.id` | `QASE_TESTOPS_PLAN_ID` | — | No |
| Batch size | `testops.batch.size` | `QASE_TESTOPS_BATCH_SIZE` | `200` | No |
| Create defects | `testops.defect` | `QASE_TESTOPS_DEFECT` | `False` | No |
| Status filter | `testops.statusFilter` | `QASE_TESTOPS_STATUS_FILTER` | — | No |
| Configuration values | `testops.configurations.values` | `QASE_TESTOPS_CONFIGURATIONS_VALUES` | — | No |
| Create configurations | `testops.configurations.createIfNotExists` | `QASE_TESTOPS_CONFIGURATIONS_CREATE_IF_NOT_EXISTS` | `false` | No |
| Show public report link | `testops.showPublicReportLink` | `QASE_TESTOPS_SHOW_PUBLIC_REPORT_LINK` | `False` | No |

\* Required when using `testops` mode

### TestOps Multi Options (Multiple Projects)

| Description | Config file | Environment variable | Default | Required |
|-------------|-------------|---------------------|---------|----------|
| Default project | `testops_multi.default_project` | `QASE_TESTOPS_MULTI_DEFAULT_PROJECT` | — | No |
| Projects array | `testops_multi.projects` | — | `[]` | Yes** |
| Project code | `testops_multi.projects[].code` | — | — | Yes** |
| Test run title | `testops_multi.projects[].run.title` | — | `Automated Run <code> <date>` | No |
| Test run description | `testops_multi.projects[].run.description` | — | `Automated Run <code> <date>` | No |
| Complete test run | `testops_multi.projects[].run.complete` | — | `True` | No |
| Test run ID | `testops_multi.projects[].run.id` | — | — | No |
| Test run tags | `testops_multi.projects[].run.tags` | — | `[]` | No |
| External link | `testops_multi.projects[].run.externalLink` | — | — | No |
| Test plan ID | `testops_multi.projects[].plan.id` | — | — | No |
| Environment | `testops_multi.projects[].environment` | — | Global | No |

\** Required when using `testops_multi` mode

**Multi-project annotations:**

| Framework | Syntax |
|-----------|--------|
| Pytest | `@qase.project_id("CODE", 1, 2, 3)` |
| Behave | `@qase.project_id.CODE:1,2,3` |
| Robot Framework | `Q-PROJECT.CODE-1,2,3` |
| Tavern | `QaseProjectID.CODE=1,2,3` in test name |

See details: [Pytest](../qase-pytest/docs/MULTI_PROJECT.md) | [Behave](../qase-behave/docs/MULTI_PROJECT.md) | [Robot Framework](../qase-robotframework/docs/MULTI_PROJECT.md) | [Tavern](../qase-tavern/docs/MULTI_PROJECT.md)

### Local Report Options

| Description | Config file | Environment variable | Default |
|-------------|-------------|---------------------|---------|
| Driver | `report.driver` | `QASE_REPORT_DRIVER` | `local` |
| Report path | `report.connection.path` | `QASE_REPORT_CONNECTION_PATH` | `./build/qase-report` |
| Report format | `report.connection.format` | `QASE_REPORT_CONNECTION_FORMAT` | `json` |

### Logging Options

| Description | Config file | Environment variable | Default |
|-------------|-------------|---------------------|---------|
| Console output | `logging.console` | `QASE_LOGGING_CONSOLE` | `True` |
| File output | `logging.file` | `QASE_LOGGING_FILE` | Same as `debug` |

### Framework-Specific Options

#### Pytest

| Description | Config file | Environment variable | CLI | Default |
|-------------|-------------|---------------------|-----|---------|
| Capture logs | `framework.pytest.captureLogs` | `QASE_PYTEST_CAPTURE_LOGS` | `--qase-pytest-capture-logs` | `False` |
| XFail status (failed) | `framework.pytest.xfailStatus.xfail` | `QASE_PYTEST_XFAIL_STATUS_XFAIL` | `--qase-pytest-xfail-status-xfail` | `Skipped` |
| XFail status (passed) | `framework.pytest.xfailStatus.xpass` | `QASE_PYTEST_XFAIL_STATUS_XPASS` | `--qase-pytest-xfail-status-xpass` | `Passed` |

#### Behave, Robot Framework, Tavern

These frameworks use only the common configuration options.

---

## Configuration Examples

### Single Project (testops)

```json
{
  "mode": "testops",
  "fallback": "report",
  "debug": false,
  "environment": "local",
  "testops": {
    "api": {
      "token": "<token>",
      "host": "qase.io"
    },
    "project": "DEMO",
    "run": {
      "title": "Regress run",
      "description": "Automated regression tests",
      "complete": true,
      "tags": ["regression", "automated"]
    },
    "batch": {
      "size": 100
    }
  }
}
```

### Multiple Projects (testops_multi)

```json
{
  "mode": "testops_multi",
  "fallback": "report",
  "testops": {
    "api": {
      "token": "<token>",
      "host": "qase.io"
    },
    "batch": {
      "size": 100
    }
  },
  "testops_multi": {
    "default_project": "DEMO1",
    "projects": [
      {
        "code": "DEMO1",
        "run": {
          "title": "DEMO1 Test Run",
          "tags": ["staging"]
        },
        "environment": "staging"
      },
      {
        "code": "DEMO2",
        "run": {
          "title": "DEMO2 Test Run",
          "tags": ["production"]
        },
        "environment": "production"
      }
    ]
  }
}
```

### Environment Variables

```bash
# Common settings
export QASE_MODE="testops"
export QASE_FALLBACK="report"
export QASE_ENVIRONMENT="local"
export QASE_DEBUG="false"

# TestOps
export QASE_TESTOPS_API_TOKEN="<token>"
export QASE_TESTOPS_PROJECT="DEMO"
export QASE_TESTOPS_RUN_TITLE="Automated Run"
export QASE_TESTOPS_RUN_COMPLETE="true"

# Pytest
export QASE_PYTEST_CAPTURE_LOGS="true"
```

---

## Profilers

Profilers automatically track operations during test execution and send them as steps to Qase TestOps.

| Profiler | Description | Documentation |
|----------|-------------|---------------|
| `network` | Tracks HTTP requests (requests, urllib3) | [Network Profiler](docs/NETWORK_PROFILER.md) |
| `db` | Tracks database operations | [Database Profiler](docs/DATABASE_PROFILERS.md) |
| `sleep` | Tracks sleep calls | — |

Enable profilers in `qase.config.json`:

```json
{
  "profilers": ["network", "db"]
}
```

Or via environment variable:

```bash
export QASE_PROFILERS="network,db"
```

The `profilers` array supports both string and object formats. Use the object format to configure profiler-specific options:

```json
{
  "profilers": [
    {
      "name": "network",
      "excludeHosts": ["telemetry.local", "monitoring.internal"]
    },
    "db"
  ]
}
```

---

## Additional Features

### Status Mapping

Allows changing test result status before sending to Qase:

```json
{
  "statusMapping": {
    "invalid": "failed",
    "skipped": "passed"
  }
}
```

**Available statuses:** `passed`, `failed`, `skipped`, `invalid`

### Status Filtering

Excludes results with specified statuses from being sent:

```json
{
  "testops": {
    "statusFilter": ["passed", "skipped"]
  }
}
```

### External Links

Associates the test run with external resources (e.g., Jira):

```json
{
  "testops": {
    "run": {
      "externalLink": {
        "type": "jiraCloud",
        "link": "PROJ-123"
      }
    }
  }
}
```

**Types:** `jiraCloud`, `jiraServer`

### Test Run Configurations

Creates or finds configurations in Qase TestOps:

```json
{
  "testops": {
    "configurations": {
      "values": [
        { "name": "browser", "value": "chrome" },
        { "name": "os", "value": "linux" }
      ],
      "createIfNotExists": true
    }
  }
}
```

---

## Requirements

- Python 3.9+
- qase-api-client

## License

Apache 2.0 — see [LICENSE](../LICENSE)
