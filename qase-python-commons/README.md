# Qase Python Commons

## Description

This module is an SDK for developing test reporters for Qase TMS.
It's using `qase-api-client` as an API client, and all Qase Python reporters are, in turn,
using this package.
You should use it if you're developing your own test reporter for a special-purpose framework.

To report results from tests using a popular framework or test runner,
don't install this module directly and
use the corresponding reporter module instead:

* [Pytest](https://github.com/qase-tms/qase-python/tree/main/qase-pytest#readme)
* [Behave](https://github.com/qase-tms/qase-python/tree/main/qase-behave#readme)
* [Robot Framework](https://github.com/qase-tms/qase-python/tree/main/qase-robotframework#readme)
* [Tavern](https://github.com/qase-tms/qase-python/tree/main/qase-tavern#readme)

## Installation

```bash
pip install qase-python-commons
```

## Configuration

Qase Python Reporters can be configured in multiple ways:

* using a config file `qase.config.json`
* using environment variables
* using command line options (for frameworks that support it, like pytest and tavern)

Environment variables override the values given in the config file,
and command line options override both other values.

All configuration options are listed in the tables below:

### Common Configuration

| Description                                                                                                           | Config file                | Environment variable            | Default value                           | Required | Possible values            |
|-----------------------------------------------------------------------------------------------------------------------|----------------------------|---------------------------------|-----------------------------------------|----------|----------------------------|
| **Common**                                                                                                            |                            |                                 |                                         |          |                            |
| Mode of reporter                                                                                                      | `mode`                     | `QASE_MODE`                     | `off`                                  | No       | `testops`, `testops_multi`, `report`, `off` |
| Fallback mode of reporter                                                                                             | `fallback`                 | `QASE_FALLBACK`                 | `off`                                   | No       | `testops`, `testops_multi`, `report`, `off` |
| Environment                                                                                                           | `environment`              | `QASE_ENVIRONMENT`              | undefined                              | No       | Any string                 |
| Root suite                                                                                                            | `rootSuite`                | `QASE_ROOT_SUITE`               | undefined                               | No       | Any string                 |
| Enable debug logs                                                                                                     | `debug`                    | `QASE_DEBUG`                    | `False`                                 | No       | `True`, `False`            |
| Execution plan path                                                                                                   | `executionPlan.path`       | `QASE_EXECUTION_PLAN_PATH`      | `./build/qase-execution-plan.json`      | No       | Any string                 |
| Exclude parameters from test results                                                                                  | `excludeParams`            | `QASE_EXCLUDE_PARAMS`           | undefined                               | No       | Comma-separated list of parameter names |
| Map test result statuses to different values (format: `fromStatus=toStatus`)                                          | `statusMapping`            | `QASE_STATUS_MAPPING`           | undefined                               | No       | Object mapping statuses (e.g., `{"invalid": "failed", "skipped": "passed"}`) |
| **Logging configuration**                                                                                             |                            |                                 |                                         |          |                            |
| Enable/disable console output for reporter logs                                                                       | `logging.console`          | `QASE_LOGGING_CONSOLE`          | `True`                                  | No       | `True`, `False`            |
| Enable/disable file output for reporter logs                                                                          | `logging.file`             | `QASE_LOGGING_FILE`             | Same as `debug` setting                 | No       | `True`, `False`            |
| **Qase Report configuration**                                                                                         |                            |                                 |                                         |          |                            |
| Driver used for report mode                                                                                           | `report.driver`            | `QASE_REPORT_DRIVER`            | `local`                                 | No       | `local`                    |
| Path to save the report                                                                                               | `report.connection.path`   | `QASE_REPORT_CONNECTION_PATH`   | `./build/qase-report`                   | No       | Any string                 |
| Local report format                                                                                                   | `report.connection.format` | `QASE_REPORT_CONNECTION_FORMAT` | `json`                                  | No       | `json`, `jsonp`            |
| **Qase TestOps configuration (single project)**                                                                       |                            |                                 |                                         |          |                            |
| Token for [API access](https://developers.qase.io/#authentication)                                                    | `testops.api.token`        | `QASE_TESTOPS_API_TOKEN`        |  undefined                              | Yes*     | Any string                 |
| Qase API host. For enterprise users, specify address: `example.qase.io`                                           | `testops.api.host`         | `QASE_TESTOPS_API_HOST`         | `qase.io`                               | No       | Any string                 |
| Code of your project, which you can take from the URL: `https://app.qase.io/project/DEMOTR` - `DEMOTR` is the project code | `testops.project`          | `QASE_TESTOPS_PROJECT`          |  undefined                              | Yes*     | Any string                 |
| Qase test run ID                                                                                                      | `testops.run.id`           | `QASE_TESTOPS_RUN_ID`           |  undefined                              | No       | Any integer                |
| Qase test run title                                                                                                   | `testops.run.title`        | `QASE_TESTOPS_RUN_TITLE`        | `Automated run <Current date and time>` | No       | Any string                 |
| Qase test run description                                                                                             | `testops.run.description`  | `QASE_TESTOPS_RUN_DESCRIPTION`  | `<Framework name> automated run`        | No       | Any string                 |
| Qase test run complete                                                                                                | `testops.run.complete`     | `QASE_TESTOPS_RUN_COMPLETE`     | `True`                                  | No       | `True`, `False`            |
| Array of tags to be added to the test run                                                                             | `testops.run.tags`         | `QASE_TESTOPS_RUN_TAGS`         | `[]`                                    | No       | Array of strings           |
| External link to associate with test run (e.g., Jira ticket)                                                          | `testops.run.externalLink` | `QASE_TESTOPS_RUN_EXTERNAL_LINK` | undefined                              | No       | JSON object with `type` (`jiraCloud` or `jiraServer`) and `link` (e.g., `PROJ-123`) |
| Qase test plan ID                                                                                                     | `testops.plan.id`          | `QASE_TESTOPS_PLAN_ID`          |  undefined                              | No       | Any integer                |
| Size of batch for sending test results                                                                                | `testops.batch.size`       | `QASE_TESTOPS_BATCH_SIZE`       | `200`                                   | No       | Any integer (1 to 2000)    |
| Enable defects for failed test cases                                                                                  | `testops.defect`           | `QASE_TESTOPS_DEFECT`           | `False`                                 | No       | `True`, `False`            |
| Filter test results by status (comma-separated list of statuses to exclude from reporting)                           | `testops.statusFilter`              | `QASE_TESTOPS_STATUS_FILTER`             | undefined                               | No       | Array of strings (`passed`, `failed`, `skipped`, `invalid`) |
| Configuration values to create/find in groups (format: `group1=value1,group2=value2`)                                | `testops.configurations.values`     | `QASE_TESTOPS_CONFIGURATIONS_VALUES`     | undefined                               | No       | Array of objects with `name` and `value` fields |
| Create configuration groups if they don't exist                                                                       | `testops.configurations.createIfNotExists` | `QASE_TESTOPS_CONFIGURATIONS_CREATE_IF_NOT_EXISTS` | `false`                          | No       | `True`, `False`            |
| Enable public report link generation and display after test run completion                                            | `testops.showPublicReportLink`      | `QASE_TESTOPS_SHOW_PUBLIC_REPORT_LINK`   | `False`                                 | No       | `True`, `False`            |
| **Qase TestOps Multi-Project configuration**                                                                          |                            |                                 |                                         |          |                            |
| Default project code for tests without explicit project mapping                                                        | `testops_multi.default_project`     | `QASE_TESTOPS_MULTI_DEFAULT_PROJECT` | undefined                              | No       | Any string (must match one of the project codes in `projects`) |
| Array of project configurations                                                                                       | `testops_multi.projects`   | N/A (use config file)           | `[]`                                    | Yes**    | Array of project configuration objects |
| Project code                                                                                                           | `testops_multi.projects[].code`     | N/A                              | undefined                              | Yes**    | Any string                 |
| Project-specific test run title                                                                                        | `testops_multi.projects[].run.title` | N/A                            | `Automated Run <project_code> <Current date and time>` | No       | Any string                 |
| Project-specific test run description                                                                                  | `testops_multi.projects[].run.description` | N/A                        | `Automated Run <project_code> <Current date and time>` | No       | Any string                 |
| Project-specific test run complete                                                                                     | `testops_multi.projects[].run.complete` | N/A                          | `True`                                  | No       | `True`, `False`            |
| Project-specific test run ID                                                                                          | `testops_multi.projects[].run.id`   | N/A                              | undefined                              | No       | Any integer                |
| Project-specific test run tags                                                                                         | `testops_multi.projects[].run.tags` | N/A                             | `[]`                                    | No       | Array of strings           |
| Project-specific external link                                                                                         | `testops_multi.projects[].run.externalLink` | N/A                        | undefined                              | No       | JSON object with `type` and `link` |
| Project-specific test plan ID                                                                                          | `testops_multi.projects[].plan.id` | N/A                              | undefined                              | No       | Any integer                |
| Project-specific environment                                                                                           | `testops_multi.projects[].environment` | N/A                          | Uses global `environment` if not set    | No       | Any string or integer (environment ID) |

\* Required when using `testops` mode  
\** Required when using `testops_multi` mode

### Framework-Specific Configuration

#### Pytest

| Description                                    | Config file                          | Environment variable             | CLI option                         | Default value                           | Required | Possible values            |
|------------------------------------------------|--------------------------------------|----------------------------------|------------------------------------|-----------------------------------------|----------|----------------------------|
| Capture logs                                   | `framework.pytest.captureLogs`       | `QASE_PYTEST_CAPTURE_LOGS`       | `--qase-pytest-capture-logs`       | `False`                                 | No       | `true`, `false`            |
| XFail status for failed tests                  | `framework.pytest.xfailStatus.xfail` | `QASE_PYTEST_XFAIL_STATUS_XFAIL` | `--qase-pytest-xfail-status-xfail` | `Skipped`                               | No       | Any string                 |
| XFail status for passed tests                  | `framework.pytest.xfailStatus.xpass` | `QASE_PYTEST_XFAIL_STATUS_XPASS` | `--qase-pytest-xfail-status-xpass` | `Passed`                                | No       | Any string                 |

#### Behave

Behave reporter uses the same common configuration options. There are no framework-specific options for Behave.

#### Robot Framework

Robot Framework reporter uses the same common configuration options. There are no framework-specific options for Robot Framework.

#### Tavern

Tavern reporter uses the same common configuration options. There are no framework-specific options for Tavern.

## Configuration Examples

### Single Project Configuration (`testops` mode)

Example `qase.config.json` config:

```json
{
  "mode": "testops",
  "fallback": "report",
  "debug": false,
  "environment": "local",
  "excludeParams": ["password", "token"],
  "statusMapping": {
    "invalid": "failed",
    "skipped": "passed"
  },
  "logging": {
    "console": true,
    "file": true
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
  "testops": {
    "api": {
      "token": "<token>",
      "host": "qase.io"
    },
    "project": "<project_code>",
    "run": {
      "title": "Regress run",
      "description": "Regress run description",
      "complete": true,
      "tags": ["tag1", "tag2"],
      "externalLink": {
        "type": "jiraCloud",
        "link": "PROJ-123"
      }
    },
    "defect": false,
    "batch": {
      "size": 100
    },
    "statusFilter": ["passed", "skipped"],
    "showPublicReportLink": true,
    "configurations": {
      "values": [
        {
          "name": "group1",
          "value": "value1"
        },
        {
          "name": "group2", 
          "value": "value2"
        }
      ],
      "createIfNotExists": true
    }
  },
  "framework": {
    "pytest": {
      "captureLogs": true,
      "xfailStatus": {
        "xfail": "Skipped",
        "xpass": "Passed"
      }
    }
  }
}
```

### Multi-Project Configuration (`testops_multi` mode)

Example `qase.config.json` config for multi-project reporting:

```json
{
  "mode": "testops_multi",
  "fallback": "report",
  "debug": false,
  "environment": "local",
  "logging": {
    "console": true,
    "file": false
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
  "testops": {
    "api": {
      "token": "<token>",
      "host": "qase.io"
    },
    "batch": {
      "size": 100
    },
    "statusFilter": ["passed"],
    "showPublicReportLink": true
  },
  "testops_multi": {
    "default_project": "DEMO1",
    "projects": [
      {
        "code": "DEMO1",
        "run": {
          "title": "DEMO1 Multi-Project Run",
          "description": "Test run for DEMO1 project",
          "complete": true,
          "tags": ["staging", "regression"],
          "externalLink": {
            "type": "jiraCloud",
            "link": "PROJ-123"
          }
        },
        "plan": {
          "id": 1
        },
        "environment": "staging"
      },
      {
        "code": "DEMO2",
        "run": {
          "title": "DEMO2 Multi-Project Run",
          "description": "Test run for DEMO2 project",
          "complete": true,
          "tags": ["production", "regression"]
        },
        "environment": "production"
      }
    ]
  }
}
```

### Environment Variables Example

```bash
# Common settings
export QASE_MODE="testops"
export QASE_FALLBACK="report"
export QASE_ENVIRONMENT="local"
export QASE_DEBUG="true"
export QASE_ROOT_SUITE="MyTestSuite"
export QASE_EXCLUDE_PARAMS="password,token"
export QASE_STATUS_MAPPING="invalid=failed,skipped=passed"

# Logging configuration
export QASE_LOGGING_CONSOLE="true"
export QASE_LOGGING_FILE="false"

# Report mode configuration
export QASE_REPORT_DRIVER="local"
export QASE_REPORT_CONNECTION_PATH="./build/qase-report"
export QASE_REPORT_CONNECTION_FORMAT="json"

# TestOps configuration (single project)
export QASE_TESTOPS_API_TOKEN="<token>"
export QASE_TESTOPS_API_HOST="qase.io"
export QASE_TESTOPS_PROJECT="DEMO"
export QASE_TESTOPS_RUN_TITLE="My Test Run"
export QASE_TESTOPS_RUN_DESCRIPTION="Test run description"
export QASE_TESTOPS_RUN_COMPLETE="true"
export QASE_TESTOPS_RUN_TAGS="tag1,tag2"
export QASE_TESTOPS_RUN_EXTERNAL_LINK='{"type":"jiraCloud","link":"PROJ-123"}'
export QASE_TESTOPS_PLAN_ID="1"
export QASE_TESTOPS_BATCH_SIZE="100"
export QASE_TESTOPS_DEFECT="false"
export QASE_TESTOPS_STATUS_FILTER="passed,skipped"
export QASE_TESTOPS_SHOW_PUBLIC_REPORT_LINK="true"

# TestOps configurations
export QASE_TESTOPS_CONFIGURATIONS_VALUES='[{"name":"browser","value":"chrome"},{"name":"os","value":"linux"}]'
export QASE_TESTOPS_CONFIGURATIONS_CREATE_IF_NOT_EXISTS="true"

# Pytest-specific
export QASE_PYTEST_CAPTURE_LOGS="true"
export QASE_PYTEST_XFAIL_STATUS_XFAIL="Skipped"
export QASE_PYTEST_XFAIL_STATUS_XPASS="Passed"

# Multi-project configuration (default project only)
export QASE_TESTOPS_MULTI_DEFAULT_PROJECT="DEMO1"
```

## Multi-Project Support

The multi-project feature allows you to send test results to multiple Qase projects simultaneously, with different test case IDs for each project. This is useful when:

* You need to report the same test to different projects
* Different projects track the same functionality with different test case IDs
* You want to maintain separate test runs for different environments or teams

### How It Works

1. Configure multiple projects in `testops_multi.projects` array
2. Each project can have its own run configuration (title, description, tags, plan, environment)
3. Use framework-specific annotations to map test cases to projects:
   * **Pytest**: Use `@qase.project_id()` decorator
   * **Behave**: Use `@qase.project_id.PROJECT_CODE:IDS` tag format
   * **Robot Framework**: Use `Q-PROJECT.PROJECT_CODE-IDS` tag format
   * **Tavern**: Use `QaseProjectID.PROJECT_CODE=IDS` format in test names
4. Tests without explicit project mapping will be sent to the `default_project`

### Framework-Specific Documentation

For detailed framework-specific documentation on multi-project support, see:

* **[Pytest Multi-Project Guide](../qase-pytest/docs/MULTI_PROJECT.md)** - Detailed guide for using multi-project support with Pytest, including decorator usage, parametrized tests, and test classes
* **[Behave Multi-Project Guide](../qase-behave/docs/MULTI_PROJECT.md)** - Detailed guide for using multi-project support with Behave, including tag formats, feature-level tags, and scenario mapping
* **[Robot Framework Multi-Project Guide](../qase-robotframework/docs/MULTI_PROJECT.md)** - Detailed guide for using multi-project support with Robot Framework, including tag formats, suite-level tags, and parameter handling
* **[Tavern Multi-Project Guide](../qase-tavern/docs/MULTI_PROJECT.md)** - Detailed guide for using multi-project support with Tavern, including test name formats, extraction rules, and troubleshooting

### Example Usage

For detailed examples, see the [multi-project examples directory](../examples/multiproject/).

## Status Mapping

You can map test result statuses to different values using the `statusMapping` configuration option. This is useful when you want to change how certain statuses are reported to Qase.

Example:

```json
{
  "statusMapping": {
    "invalid": "failed",
    "skipped": "passed"
  }
}
```

This will map:

* `invalid` status → `failed` in Qase
* `skipped` status → `passed` in Qase

## Status Filtering

You can filter out test results by status using the `testops.statusFilter` configuration option. Results with statuses in the filter list will not be sent to Qase.

Example:

```json
{
  "testops": {
    "statusFilter": ["passed", "skipped"]
  }
}
```

This will exclude all `passed` and `skipped` results from being reported to Qase.

## External Links

You can associate external links (e.g., Jira tickets) with test runs using the `testops.run.externalLink` configuration.

Example:

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

Supported types:

* `jiraCloud` - For Jira Cloud
* `jiraServer` - For Jira Server

## Configurations

You can specify test run configurations that will be created or found in Qase TestOps.

Example:

```json
{
  "testops": {
    "configurations": {
      "values": [
        {
          "name": "browser",
          "value": "chrome"
        },
        {
          "name": "os",
          "value": "linux"
        }
      ],
      "createIfNotExists": true
    }
  }
}
```

If `createIfNotExists` is `true`, configuration groups and values will be created automatically if they don't exist.
