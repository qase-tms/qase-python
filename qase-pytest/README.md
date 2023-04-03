# [Qase](https://qase.io) Pytest Plugin

[![License](https://lxgaming.github.io/badges/License-Apache%202.0-blue.svg)](https://www.apache.org/licenses/LICENSE-2.0)

# Installation

```
pip install qase-pytest
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

To link tests in code with tests in Qase TestOps you can use predefined decorators:

```python
from qaseio.pytest import qase

@qase.id(13)
@qase.title("My first test")
@qase.severity("critical")
@qase.layer("unit")
@qase.precondition("*Precondition 1*. Markdown is supported.")
@qase.description("Try to login in Qase TestOps using login and password")
def test_example_1():
    pass
```

Each unique number can only be assigned once to the class or function being used.

### Ignore a particular test
If you want to exclude a particular test from the report, you can use the `@qase.ignore` decorator:

```python
from qaseio.pytest import qase

@qase.ignore
def test_example_1():
    pass
```

### Possible test result statuses

- PASSED - when test passed
- FAILED - when test failed with AssertionError
- BLOCKED - when test failed with any other exception
- SKIPPED - when test has been skipped

## Add attachments to test results

When you need to push some additional information to server you could use
attachments:

```python
import pytest
from qaseio.pytest import qase


@pytest.fixture(scope="session")
def driver():
    driver = webdriver.Chrome()
    yield driver
    logs = "\n".join(str(row) for row in driver.get_log('browser')).encode('utf-8')
    qase.attach((logs, "text/plain", "browser.log"))
    driver.quit()

@qase.title("My first test")
def test_example_1():
    qase.attach("/path/to/file", "/path/to/file/2")
    qase.attach(
        ("/path/to/file/1", "application/json"),
        ("/path/to/file/3", "application/xml"),
    )

@qase.id(12)
def test_example_2(driver):
    qase.attach((driver.get_screenshot_as_png(), "image/png", "result.png"))
```

You could pass as much files as you need.

Also you should know, that if no case id is associated with current test in
pytest - attachment would not be uploaded:

```python
import pytest
from qaseio.pytest import qase


@pytest.fixture(scope="session")
def driver():
    driver = webdriver.Chrome()
    yield driver
    logs = "\n".join(str(row) for row in driver.get_log('browser')).encode('utf-8')
    # This would do nothing, because last test does not have case id link
    qase.attach((logs, "text/plain", "browser.log"))
    driver.quit()

def test_example_2(driver):
    # This would do nothing
    qase.attach((driver.get_screenshot_as_png(), "image/png", "result.png"))
```

## Linking code with steps

It is possible to link test step with function, or using context.

```python
from qaseio.pytest import qase

@qase.step("First step") # test step name
def some_step():
    sleep(5)

@qase.step("Second step")  # test step name
def another_step():
    sleep(3)

...

def test_example():
    some_step()
    another_step()
    # test step hash
    with qase.step("Third step"):
        sleep(1)
```

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
