# Qase Pytest Plugin configuration

Qase Pytest Plugin can be configured in multiple ways:
 - using a config file `qase.config.json`
 - using environment variables
 - using CLI options

All configuration options are listed in the table below:
| Description | Config file | Environment variable | CLI option | Default value | Required | Possible values |
| --- | --- | --- | --- | --- | --- | --- |
| **Common** |
| Mode of reporter | `mode` | `QASE_MODE` | `--qase-mode` | `testops` | No | `testops`, `report`, `off` |
| Fallback mode | `fallback` | `QASE_FALLBACK` | `--qase-fallback` | `report` | No | `report`, `off` |
| Environment | `environment` | `QASE_ENVIRONMENT` | `--qase-environment` | `local` | No | Any string |
| Execution plan path | `execution_plan_path` | `QASE_EXECUTION_PLAN_PATH` | `--qase-execution-plan-path` | `./build/qase-execution-plan.json` | No | Any string |
| **Qase Report configuration** |
| Report driver | `report.driver` | `QASE_REPORT_DRIVER` | `--qase-report-driver` | `local` | No | `local` |
| Local path to store report | `report.connection.path` | `QASE_REPORT_CONNECTION_PATH` | `--qase-report-connection-path` | `./build/qase-report` | No | Any string |
| Report format | `report.connection.format` | `QASE_REPORT_CONNECTION_FORMAT` | `--qase-report-connection-format` | `json` | No | `json`, `jsonp` |
| **Qase TestOps configuration** |
| TestOps API token | `testops.api.token` | `QASE_TESTOPS_API_TOKEN` | `--qase-testops-api-token` |  | Yes | Any string |
| TestOps API host | `testops.api.host` | `QASE_TESTOPS_API_HOST` | `--qase-testops-api-host` | `qase.io` | No | Any string |
| TestOps project code | `testops.project` | `QASE_TESTOPS_PROJECT` | `--qase-testops-project` |  | Yes | Any string |
| TestOps test run ID | `testops.run.id` | `QASE_TESTOPS_RUN_ID` | `--qase-testops-run-id` |  | No | Any integer |
| TestOps test run title | `testops.run.title` | `QASE_TESTOPS_RUN_TITLE` | `--qase-testops-run-title` |  | No | Any string |
| TestOps test run description | `testops.run.description` | `QASE_TESTOPS_RUN_DESCRIPTION` | `--qase-testops-run-description` |  | No | Any string |
| TestOps test run complete | `testops.run.complete` | `QASE_TESTOPS_RUN_COMPLETE` | `--qase-testops-run-complete` | `True` | No | `true`, `false` |
| TestOps test plan ID | `testops.plan.id` | `QASE_TESTOPS_PLAN_ID` | `--qase-testops-plan-id` |  | No | Any integer |
| Execution chunk size | `testops.chunk` | `QASE_TESTOPS_CHUNK` | `--qase-testops-chunk` | `200` | No | Any integer |
| TestOps defect | `testops.defect` | `QASE_TESTOPS_DEFECT` | `--qase-testops-defect` | `True` | No | `true`, `false` |
| TestOps bulk | `testops.bulk` | `QASE_TESTOPS_BULK` | `--qase-testops-bulk` | `True` | No | `true`, `false` |
| **Framework specific options** |
| **Pytest** |
| Capture logs | `pytest.capture_logs` | `QASE_PYTEST_CAPTURE_LOGS` | `--qase-pytest-capture-logs` | `False` | No | `true`, `false` |
| Capture HTTP traffic | `pytest.capture_http` | `QASE_PYTEST_CAPTURE_HTTP` | `--qase-pytest-capture-http` | `False` | No | `true`, `false` |
