# Qase Robot Framework Plugin configuration

Qase Robot Framework Reporter is configured in multiple ways:

- using a config file `qase.config.json`
- using environment variables

Environment variables override the values given in the config file.

## Configuration options

| Description                               | Config file                | Environment variable            | Default value                           | Required | Possible values            |
|-------------------------------------------|----------------------------|---------------------------------|-----------------------------------------|----------|----------------------------|
| **Common**                                |
| Main reporting mode                       | `mode`                     | `QASE_MODE`                     | `off`                               | No       | `testops`, `report`, `off` |
| Fallback reporting mode                   | `fallback`                 | `QASE_FALLBACK`                 | `report`                                | No       | `testops`, `report`, `off` |
| Execution plan path                       | `executionPlan.path`       | `QASE_EXECUTION_PLAN_PATH`      | `./build/qase-execution-plan.json`      | No       | Any string                 |
| Qase environment                          | `environment`              | `QASE_ENVIRONMENT`              | `local`                                 | No       | Any string                 |
| Root suite                                | `rootSuite`                | `QASE_ROOT_SUITE`               |                                         | No       | Any string                 |
| Debug logs                                | `debug`                    | `QASE_DEBUG`                    | `False`                                 | No       | `True`, `False`            |
| Exclude parameters from test results      | `excludeParams`           | `QASE_EXCLUDE_PARAMS`           | None, don't exclude any parameters      | No       | Comma-separated list of parameter names |
| **Logging configuration**                |
| Enable/disable console logging output     | `logging.console`         | `QASE_LOGGING_CONSOLE`          | `true`                                  | No       | `true`, `false`            |
| Enable/disable file logging output         | `logging.file`             | `QASE_LOGGING_FILE`             | `false` (true when debug=true)          | No       | `true`, `false`            |
| **Qase TestOps mode configuration**       |
| Qase project code                         | `testops.project`          | `QASE_TESTOPS_PROJECT`          |                                         | Yes      | Any string                 |
| Qase API token                            | `testops.api.token`        | `QASE_TESTOPS_API_TOKEN`        |                                         | Yes      | Any string                 |
| Qase API host. For enterprise users, specify address: `example.qase.io`                            | `testops.api.host`         | `QASE_TESTOPS_API_HOST`         | `qase.io`                               | No       | Any string                 |
| Title of the Qase test run                | `testops.run.title`        | `QASE_TESTOPS_RUN_TITLE`        | `Automated Run {current date and time}` | No       | Any string                 |
| Description of the Qase test run          | `testops.run.description`  | `QASE_TESTOPS_RUN_DESCRIPTION`  | None, leave empty                       | No       | Any string                 |
| Create test run using a test plan         | `testops.plan.id`          | `QASE_TESTOPS_PLAN_ID`          | None, don't use plans for the test run  | No       | Any integer                |
| Complete test run after running tests     | `testops.run.complete`     | `QASE_TESTOPS_RUN_COMPLETE`     | `True`                                  | No       | `true`, `false`            |
| ID of the Qase test run to report results | `testops.run.id`           | `QASE_TESTOPS_RUN_ID`           | None, create a new test run             | No       | Any integer                |
| External link type for test run           | `testops.run.externalLink.type` | `QASE_TESTOPS_RUN_EXTERNAL_LINK_TYPE` | None, don't add external link           | No       | `jiraCloud`, `jiraServer`   |
| External link URL for test run            | `testops.run.externalLink.link` | `QASE_TESTOPS_RUN_EXTERNAL_LINK_URL` | None, don't add external link           | No       | Any string (e.g., "PROJ-1234") |
| Batch size for uploading test results     | `testops.batch.size`       | `QASE_TESTOPS_BATCH_SIZE`       | 200                                     | No       | 1 to 2000                  |
| Create defects in Qase                    | `testops.defect`           | `QASE_TESTOPS_DEFECT`           | `False`, don't create defects           | No       | `True`, `False`            |
| Test run tags                             | `testops.run.tags`         | `QASE_TESTOPS_RUN_TAGS`         | None, don't add any tags                | No       | Comma-separated list of tags |
| Test run configurations                   | `testops.configurations.values` | `QASE_TESTOPS_CONFIGURATIONS_VALUES` | None, don't add any configurations      | No       | Format: "group1=value1,group2=value2" |
| Create configurations if not exists       | `testops.configurations.createIfNotExists` | `QASE_TESTOPS_CONFIGURATIONS_CREATE_IF_NOT_EXISTS` | `False`, don't create configurations     | No       | `True`, `False`            |
| Filter results by status                  | `testops.statusFilter`     | `QASE_TESTOPS_STATUS_FILTER`    | None, don't filter any results          | No       | Comma-separated list of statuses |
| **Qase Report mode configuration**        |
| Local path to store report                | `report.connection.path`   | `QASE_REPORT_CONNECTION_PATH`   | `./build/qase-report`                   | No       | Any string                 |
| Report format                             | `report.connection.format` | `QASE_REPORT_CONNECTION_FORMAT` | `json`                                  | No       | `json`, `jsonp`            |
| Driver used for report mode               | `report.driver`            | `QASE_REPORT_DRIVER`            | `local`                                 | No       | `local`                    |

## Example `qase.config.json` config:

```json
{
  "mode": "testops",
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
    "run": {
      "title": "Regress run",
      "description": "Regress run description",
      "complete": true,
      "tags": ["tag1", "tag2"],
      "externalLink": {
        "type": "jiraCloud",
        "link": "PROJ-1234"
      }
    },
    "defect": false,
    "project": "<project_code>",
    "batch": {
      "size": 100
    },
    "statusFilter": ["passed", "failed"],
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
  }
}
```
