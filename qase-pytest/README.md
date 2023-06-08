# [Qase](https://qase.io) Pytest Plugin

[![License](https://lxgaming.github.io/badges/License-Apache%202.0-blue.svg)](https://www.apache.org/licenses/LICENSE-2.0)

## Installation

```
pip install qase-pytest
```

## Upgrade from 4.x to 5.x
A new version of qase-pytest reporter has breaking changes. Follow these [guide](UPGRADE.md) that will help you to migrate to a new version.

## Configuration

Qase Pytest Plugin can be configured in multiple ways:
 - using a config file `qase.config.json`
 - using environment variables
 - using CLI options

All configuration options are listed in the following doc: [Configuration](../README.md#configuration).


### Example: qase.config.json

```
{
	"mode": "testops", 
	"fallback": "report",
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
		"bulk": true,
		"api": {
			"token": "YOUR_API_TOKEN",
			"host": "qase.io"
		},
		"run": {
            "id": 1,
			"title": "Test run title",
			"complete": true
		},
        "plan": {
            "id": 1
        },
		"defect": true,
		"project": "YOUR_PROJECT_CODE",
		"chunk": 200
	},
	"framework": {
		"pytest": {
			"capture": {
				"logs": true,
				"http": true
			}
		}
	},
	"environment": "local"
}
```

## Usage

### Link tests with test cases in Qase TestOps

To link tests in code with tests in Qase TestOps you can use predefined decorators:

```python
from qaseio.pytest import qase

@qase.id(13)
@qase.title("My first test")
@qase.fields(
    ("severity", "critical"),
    ("priority", "hight"),
    ("layer", "unit"),
    ("description", "Try to login in Qase TestOps using login and password"),
    ("description", "*Precondition 1*. Markdown is supported."),
)
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

### Capture network logs
In order to capture network logs, you need to enable the `http` option in the `capture` section of the `framework` section in the config file.

Qase Pytest reporter will capture all requests and responses and save as a test step automatically.

### Add attachments to test results

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

### Linking code with steps

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

### Sending tests to existing testrun

Testrun in TestOps will contain only those test results, which are presented in testrun,
but every test would be executed.

```bash
pytest \
    --qase-mode=testops \
    --qase-testops-api-token=<your api token here> \
    --qase-testops-project=PRJCODE \ # project, where your testrun exists in
    --qase-testops-run-id=3 # testrun id
```

### Creating test run base on test plan (selective launch)

Create new testrun base on testplan. Testrun in Qase TestOps will contain only those
test results. `qase-pytest` supports selective execution

```bash
pytest \
    --qase-mode=testops \
    --qase-testops-api-token=<your api token here> \
    --qase-testops-project=PRJCODE \ # project, where your testrun exists in
    --qase-testops-plan-id=3 # testplan id
```

### Creating new testrun according to current pytest run

If you want to create a new test run in Qase TestOps for each execution, you can simply 
skip `--qase-testops-run` option. If you want to provide a custom name for this run, you can add an
option `--qase-testops-run-title` 

```bash
pytest \
    --qase-mode=testops \
    --qase-testops-api-token=<your api token here> \
    --qase-testops-project=PRJCODE \ # project, where your testrun would be created
    --qase-testops-run-title=My\ First\ Automated\ Run
```
