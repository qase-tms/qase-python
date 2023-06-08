# [Qase](https://qase.io) Pytest-bdd Plugin

[![License](https://lxgaming.github.io/badges/License-Apache%202.0-blue.svg)](https://www.apache.org/licenses/LICENSE-2.0)

# Installation

```
pip install qase-pytest-bdd
```

# Usage

### Command-line arguments
Configuration could be provided both by `pytest.ini`/`tox.ini` params
and using command-line arguments:

* Command-line args:
```
  --qase-mode           Define mode: `testops` to enable report
  --qase-environment=QS_ENVIRONMENT
                        Define execution environment ID
  --qase-to-api-token=QS_TO_API_TOKEN
                        Api token for Qase TestOps
  --qase-to-project=QS_TO_PROJECT
                        Project code in Qase TestOps
  --qase-to-run=QS_TO_RUN_ID
                        Test Run ID in Qase TestOps
  --qase-to-run-title=QS_TO_RUN_TITLE
                        Define a custom title for Qase Test Run
  --qase-to-plan=QS_TO_PLAN_ID
                        Test Plan ID in Qase TestOps
  --qase-to-complete-run
                        Complete run after all tests are finished
  --qase-to-mode=QS_TO_MODE
                        You can choose `sync` or `async` mode for results publication. Default: `async`
  --qase-to-host=QS_TO_HOST
                        Qase TestOps Enterprise customers can set their own hosts. Default: `qase.io`
```

* INI file parameters:

```
  qs_mode (string):     default value for --qase-mode
  qs_environment (string):
                        default value for --qase-environment
  qs_to_api_token (string):
                        default value for --qase-to-api-token
  qs_to_project (string):
                        default value for --qase-to-project
  qs_to_run_id (string):
                        default value for --qase-to-run
  qs_to_run_title (string):
                        default value for --qase-to-run-title
  qs_to_plan_id (string):
                        default value for --qase-to-plan
  qs_to_complete_run (bool):
                        default value for --qase-to-complete-run
  qs_to_mode (string):
                        default value for --qase-to-mode
  qs_to_host (string):
                        default value for --qase-to-host
    
```

## Link tests with test cases in Qase TestOps


### Ignore a particular test


### Possible test result statuses

- PASSED - when test passed
- FAILED - when test failed with AssertionError
- BLOCKED - when test failed with any other exception
- SKIPPED - when test has been skipped

## Add attachments to test results

## Linking code with steps

## Sending tests to existing testrun

Testrun in TestOps will contain only those test results, which are presented in testrun,
but every test would be executed.

```bash
pytest \
    --qase-mode=testops \
    --qase-to-api-token=<your api token here> \
    --qase-to-project=PRJCODE \ # project, where your testrun exists in
    --qase-to-run=3 # testrun id
```

## Creating test run base on test plan

Create new testrun base on testplan. Testrun in Qase TestOps will contain only those
test results, which are presented in testrun, but every test would be executed.

```bash
pytest \
    --qase-mode=testops \
    --qase-to-api-token=<your api token here> \
    --qase-to-project=PRJCODE \ # project, where your testrun exists in
    --qase-to-plan=3 # testplan id
```

## Creating new testrun according to current pytest run

If you want to create a new test run in Qase TestOps for each execution, you can simply 
skip `--qase-to-run`. If you want to provide a custom name for this run, you can add an
option `--qase-to-run-title` 

```bash
pytest \
    --qase-mode=testops \
    --qase-to-api-token=<your api token here> \
    --qase-to-project=PRJCODE \ # project, where your testrun would be created
    --qase-to-run-title=My\ First\ Automated\ Run
```

## Qase TestOps submission mode

Qase Pytest plugin for TestOps can work in two different modes: `sync` or `async`. 

*Sync* sends each result to Qase TestOps API right after particular test execution. This mode allows you to see the results in realtime, even before test run is fully executed. 

*Async* mode sends the results of test execution when the test run is complete. It uses bulk method that dramatically reduces reporting time.
