# [Qase TestOps](https://qase.io) Pytest Reporter

[![License](https://lxgaming.github.io/badges/License-Apache%202.0-blue.svg)](https://www.apache.org/licenses/LICENSE-2.0)

## Installation

To install the latest version, run:

```sh
pip install pre qase-pytest
```

## Upgrade from 4.x to 5.x and to 6.x

The new version 6.x of the Pytest reporter has breaking changes.
To migrate from versions 4.x or 5.x, follow the [upgrade guide](docs/UPGRADE.md).

## Configuration

Qase Pytest Reporter is configured in multiple ways:

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
  "framework": {
    "pytest": {
      "captureLogs": true
    }
  },
  "environment": "local"
}
```

## Usage

For detailed instructions on using annotations and methods, refer to [Usage](docs/usage.md).

### Link tests with test cases in Qase TestOps

To link the automated tests with the test cases in Qase TestOps, use the `@qase.id()` decorator.
Other test data, such as case title, system and custom fields,
can be added with `@qase.title()` and `@qase.fields()`:

```python
from qase.pytest import qase

@qase.id(13)
@qase.title("My first test")
@qase.fields(
    ("severity", "critical"),
    ("priority", "high"),
    ("layer", "unit"),
    ("description", "Try to login to Qase TestOps using login and password"),
    ("preconditions", "*Precondition 1*. Markdown is supported."),
)
def test_example_1():
    pass

@qase.id([14, 15])
def test_example_2():
    pass
```

Each unique number can only be assigned once to the class or function being used.

### Ignore a particular test

To exclude a particular test from the report, use the `@qase.ignore` decorator:

```python
from qase.pytest import qase

@qase.ignore
def test_example_1():
    pass
```

### Possible test result statuses

- PASSED - when test passed
- FAILED - when test failed with `AssertionError`
- BLOCKED - when test failed with any other exception
- SKIPPED - when test has been skipped

### Capture network logs

To capture the network logs, enable the `http` option in the `framework.capture` section
of the configuration file.

The Qase Pytest reporter will capture all HTTP requests and responses
and save them as a test steps automatically.

### Add attachments to test results

To upload screenshots, logs, and other information to Qase.io,
use `qase.attach()`.
It works both with files in the filesystem and with data available in the code.
There is no limit on the amount of attachments from a single test.

```python
import pytest
from qase.pytest import qase

@qase.title("File attachments")
def test_example_1():
    # attach files from the filesystem:
    qase.attach("/path/to/file", "/path/to/file/2")
    # to add multiple attachments, pass them in tuples:
    qase.attach(
        ("/path/to/file/1", "application/json"),
        ("/path/to/file/3", "application/xml"),
    )

@pytest.fixture(scope="session")
def driver():
    driver = webdriver.Chrome()
    yield driver
    logs = "\n".join(str(row) for row in driver.get_log('browser')).encode('utf-8')
    # attach logs from a code variable as a text file:
    qase.attach((logs, "text/plain", "browser.log"))
    driver.quit()

@qase.id(12)
def test_example_2(driver):
    # attach the output of driver.get_screenshot_as_png() as a png image
    qase.attach((driver.get_screenshot_as_png(), "image/png", "result.png"))
```

### Linking code with steps

To mark a test step, either annotate a function with `@qase.step()`,
or use the `with qase.step()` context:

```python
from qase.pytest import qase

@qase.step("First step") # test step name
def some_step():
    sleep(5)

@qase.step("Second step")  # test step name
def another_step():
    sleep(3)

# ...

def test_example():
    some_step()
    another_step()
    # test step hash
    with qase.step("Third step"):
        sleep(1)
```

### Creating new testrun according to current pytest run

By default, qase-pytest will create a new test run in Qase TestOps
and report results to this test run.
To provide a custom name for this run, add
the option `--qase-testops-run-title`.

```bash
pytest \
    --qase-mode=testops \
    --qase-testops-api-token=<your api token here> \
    --qase-testops-project=PRJCODE \ # project, where your testrun would be created
    --qase-testops-run-title=My\ First\ Automated\ Run
```

### Sending tests to existing testrun

Test results can be reported to an existing test run in Qase using its ID.
This is useful when a test run combines tests from multiple sources:

* manual and automated
* autotests from different frameworks
* tests running in multiple shards on different machines

For example, if the test run has ID=3, the following command will
run tests and report results to this test run:

```bash
pytest \
    --qase-mode=testops \
    --qase-testops-api-token=<your api token here> \
    --qase-testops-project=PRJCODE \ # project, where the test run is created
    --qase-testops-run-id=3 # testrun id
```

### Creating test run based on test plan (selective launch)

Create a new testrun base on a testplan. Testrun in Qase TestOps will contain only those
test results. `qase-pytest` supports selective execution.

```bash
pytest \
    --qase-mode=testops \
    --qase-testops-api-token=<your api token here> \
    --qase-testops-project=PRJCODE \ # project, where your testrun exists in
    --qase-testops-plan-id=3 # testplan id
```
