# Qase Behave Plugin configuration

Qase Behave Reporter is configured in multiple ways:

- using a config file `qase.config.json`
- using environment variables
- using command line options

Environment variables override the values given in the config file,
and command line options override both other values.

## Configuration options

| Description                               | Config file                | Environment variable            | CLI option                      | Default value                           | Required | Possible values            |
|-------------------------------------------|----------------------------|---------------------------------|---------------------------------|-----------------------------------------|----------|----------------------------|
| **Common**                                |
| Main reporting mode                       | `mode`                     | `QASE_MODE`                     | `qase-mode`                     | `off`                               | No       | `testops`, `report`, `off` |
| Fallback reporting mode                   | `fallback`                 | `QASE_FALLBACK`                 | `qase-fallback`                 | `report`                                | No       | `testops`, `report`, `off` |
| Execution plan path                       | `executionPlan.path`       | `QASE_EXECUTION_PLAN_PATH`      | `qase-execution-plan-path`      | `./build/qase-execution-plan.json`      | No       | Any string                 |
| Qase environment                          | `environment`              | `QASE_ENVIRONMENT`              | `qase-environment`              | `local`                                 | No       | Any string                 |
| Root suite                                | `rootSuite`                | `QASE_ROOT_SUITE`               | `qase-root-suite`               |                                         | No       | Any string                 |
| Debug logs                                | `debug`                    | `QASE_DEBUG`                    | `qase-debug`                    | `False`                                 | No       | `True`, `False`            |
| Exclude parameters from test results      | `exclude.params`           | `QASE_EXCLUDE_PARAMS`           | `qase-exclude-params`           | None, don't exclude any parameters      | No       | Comma-separated list of parameter names |
| **Qase TestOps mode configuration**       |
| Qase project code                         | `testops.project`          | `QASE_TESTOPS_PROJECT`          | `qase-testops-project`          |                                         | Yes      | Any string                 |
| Qase API token                            | `testops.api.token`        | `QASE_TESTOPS_API_TOKEN`        | `qase-testops-api-token`        |                                         | Yes      | Any string                 |
| Qase API host                             | `testops.api.host`         | `QASE_TESTOPS_API_HOST`         | `qase-testops-api-host`         | `qase.io`                               | No       | Any string                 |
| Title of the Qase test run                | `testops.run.title`        | `QASE_TESTOPS_RUN_TITLE`        | `qase-testops-run-title`        | `Automated Run {current date and time}` | No       | Any string                 |
| Description of the Qase test run          | `testops.run.description`  | `QASE_TESTOPS_RUN_DESCRIPTION`  | `qase-testops-run-description`  | None, leave empty                       | No       | Any string                 |
| Create test run using a test plan         | `testops.plan.id`          | `QASE_TESTOPS_PLAN_ID`          | `qase-testops-plan-id`          | None, don't use plans for the test run  | No       | Any integer                |
| Complete test run after running tests     | `testops.run.complete`     | `QASE_TESTOPS_RUN_COMPLETE`     | `qase-testops-run-complete`     | `True`                                  | No       | `True`, `False`            |
| ID of the Qase test run to report results | `testops.run.id`           | `QASE_TESTOPS_RUN_ID`           | `qase-testops-run-id`           | None, create a new test run             | No       | Any integer                |
| Batch size for uploading test results     | `testops.batch.size`       | `QASE_TESTOPS_BATCH_SIZE`       | `qase-testops-batch-size`       | 200                                     | No       | 1 to 2000                  |
| Create defects in Qase                    | `testops.defect`           | `QASE_TESTOPS_DEFECT`           | `qase-testops-defect`           | `False`, don't create defects           | No       | `True`, `False`            |
| Test run tags                             | `testops.run.tags`         | `QASE_TESTOPS_RUN_TAGS`         | `qase-testops-run-tags`         | None, don't add any tags                | No       | Comma-separated list of tags |
| **Qase Report mode configuration**        |
| Local path to store report                | `report.connection.path`   | `QASE_REPORT_CONNECTION_PATH`   | `qase-report-connection-path`   | `./build/qase-report`                   | No       | Any string                 |
| Report format                             | `report.connection.format` | `QASE_REPORT_CONNECTION_FORMAT` | `qase-report-connection-format` | `json`                                  | No       | `json`, `jsonp`            |
| Driver used for report mode               | `report.driver`            | `QASE_REPORT_DRIVER`            | `qase-report-driver`            | `local`                                 | No       | `local`                    |
