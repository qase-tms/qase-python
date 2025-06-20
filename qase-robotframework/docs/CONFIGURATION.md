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
| Exclude parameters from test results      | `excludeParams`           | `QASE_EXCLUDE_PARAMS`           | None, don't exclude any parameters      | No       | Comma-separated list of parameter names |
| **Qase TestOps mode configuration**       |
| Qase project code                         | `testops.project`          | `QASE_TESTOPS_PROJECT`          |                                         | Yes      | Any string                 |
| Qase API token                            | `testops.api.token`        | `QASE_TESTOPS_API_TOKEN`        |                                         | Yes      | Any string                 |
| Qase API host. For enterprise users, specify address: `example.qase.io`                            | `testops.api.host`         | `QASE_TESTOPS_API_HOST`         | `qase.io`                               | No       | Any string                 |
| Title of the Qase test run                | `testops.run.title`        | `QASE_TESTOPS_RUN_TITLE`        | `Automated Run {current date and time}` | No       | Any string                 |
| Description of the Qase test run          | `testops.run.description`  | `QASE_TESTOPS_RUN_DESCRIPTION`  | None, leave empty                       | No       | Any string                 |
| Create test run using a test plan         | `testops.plan.id`          | `QASE_TESTOPS_PLAN_ID`          | None, don't use plans for the test run  | No       | Any integer                |
| Complete test run after running tests     | `testops.run.complete`     | `QASE_TESTOPS_RUN_COMPLETE`     | `True`                                  | No       | `true`, `false`            |
| ID of the Qase test run to report results | `testops.run.id`           | `QASE_TESTOPS_RUN_ID`           | None, create a new test run             | No       | Any integer                |
| Batch size for uploading test results     | `testops.batch.size`       | `QASE_TESTOPS_BATCH_SIZE`       | 200                                     | No       | 1 to 2000                  |
| Create defects in Qase                    | `testops.defect`           | `QASE_TESTOPS_DEFECT`           | `False`, don't create defects           | No       | `True`, `False`            |
| Test run tags                             | `testops.run.tags`         | `QASE_TESTOPS_RUN_TAGS`         | None, don't add any tags                | No       | Comma-separated list of tags |
| **Qase Report mode configuration**        |
| Local path to store report                | `report.connection.path`   | `QASE_REPORT_CONNECTION_PATH`   | `./build/qase-report`                   | No       | Any string                 |
| Report format                             | `report.connection.format` | `QASE_REPORT_CONNECTION_FORMAT` | `json`                                  | No       | `json`, `jsonp`            |
| Driver used for report mode               | `report.driver`            | `QASE_REPORT_DRIVER`            | `local`                                 | No       | `local`                    |
