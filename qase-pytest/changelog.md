# qase-pytest 7.0.0

## What's new

- Unsupport Python 3.7 and 3.8. Support Python 3.9, 3.10, 3.11, 3.12, 3.13.
- Updated the `qase-python-commons` dependency to the latest version.

# qase-pytest 6.3.10

## What's new

- Added support for updating external link for a test run.
- Updated dependency on qase-python-commons to version 3.5.6.

# qase-pytest 6.3.9

## What's new

- Improved test failure status handling
- Enhanced error classification to distinguish assertion errors from other failures
- Assertion errors (AssertionError) now map to `failed` status
- Non-assertion errors (setup failures, exceptions, etc.) now map to `invalid` status
- Updated dependency on qase-python-commons to version 3.5.5

## Migration Guide

The plugin now provides more accurate test result reporting by distinguishing between:
- `failed`: Test failed due to assertion error (test logic issue)
- `invalid`: Test failed due to non-assertion error (infrastructure/setup issue)

This change provides better insights into test failures and helps identify whether issues are related to test logic or infrastructure problems.

# qase-pytest 6.3.8

## What's new

- Added support for filtering test results by status.

# qase-pytest 6.3.7

## What's new

Fixed an issue where the plugin would crash with `TypeError: 'ExceptionChainRepr' object is not subscriptable` when handling skip messages in newer versions of pytest. The plugin now properly handles both tuple/list format longrepr (old pytest versions) and ExceptionChainRepr format (new pytest versions) for skip message extraction.

# qase-pytest 6.3.6

## What's new

- Added new decorator `qase.ignore_parameters` that allows to ignore specific parameters in Qase reports.
- The decorator can be used in combination with existing `qase.parametrize_ignore` decorator.
- Support for ignoring multiple parameters at once.

```python
@pytest.mark.parametrize("browser", ["chrome", "firefox"])
@pytest.mark.parametrize("user", ["user1", "user2"])
@qase.ignore_parameters("user", "browser")
def test_login(browser, user):
    # Both browser and user parameters will be ignored in Qase reports
    pass
```

You can also ignore only specific parameters:

```python
@pytest.mark.parametrize("browser", ["chrome", "firefox"])
@pytest.mark.parametrize("user", ["user1", "user2"])
@qase.ignore_parameters("user")
def test_login(browser, user):
    # Only user parameter will be ignored, browser will be included
    pass
```

# qase-pytest 6.3.5

## What's new

- Added support for test run configurations. You can now specify configurations when creating test runs.
- Configurations can be specified in `qase.config.json`, environment variables, or CLI parameters.
- Support for automatic creation of configurations if they don't exist (controlled by `createIfNotExists` option).

Example configuration:

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
          "name": "environment", 
          "value": "staging"
        }
      ],
      "createIfNotExists": true
    }
  }
}
```

Environment variable format: `QASE_TESTOPS_CONFIGURATIONS_VALUES="browser=chrome,environment=staging"`
CLI parameter format: `--qase-testops-configurations-values="browser=chrome,environment=staging"`

# qase-pytest 6.3.4

## What's new

- Added support for indirect parameters in `qase.parametrize_ignore` decorator.

# qase-pytest 6.3.3

## What's new

- Added support for test run tags.
- Added support for excluding parameters from test results.

# qase-pytest 6.3.2

## What's new

Added new decorator `qase.parametrize_ignore` that allows to ignore specific parameters in Qase reports while still collecting other parameters.

```python
@pytest.mark.parametrize("browser", ["chrome", "firefox", "safari"])
@qase.parametrize_ignore("test_data", ["data1", "data2", "data3"])
def test_login(browser, test_data):
    # test_data will be ignored in Qase report
    # browser parameter will be included in the report
    pass
```

The decorator can be used with any number of parameters. Only parameters specified in `qase.parametrize_ignore` will be excluded from the report.

# qase-pytest 6.3.1

## What's new

Added support specifing test parameters using `qase.param` method inside the test body.

```python
def test_example():
    qase.param("foo", "bar")
    qase.param("baz", "qux")
    pass

def test_example(param1: str):
    qase.param("param1", param1)
    pass    
```

# qase-pytest 6.3.0

## What's new

- Updated core package to the latest supported versions.
- Improved logic for handling multiple QaseID values in test results.
- Removed `useV2` configuration option. The reporter now always uses API v2 for sending results.

# qase-pytest 6.2.2

## What's new

- Logging of host system details to improve debugging and traceability.  
- Output of installed packages in logs for better environment visibility.

# qase-pytest 6.2.1

## What's new

When specifying a reason in xfail or skip marks, this reason will be added to the result comment.

# qase-pytest 6.2.0

## What's new

Updated `qase.id()` decorator to support a list of integers, allowing one test to be linked to multiple test cases.

```python
@qase.id([2, 3])
def test_example():
    pass
```

# qase-pytest 6.1.15

## What's new

Resolved an issue where a failure message for attachment uploads was displayed even when attachments were disabled in
the configuration.

# qase-pytest 6.1.14

## What's new

Resolved an issue in the pytest plugin where an KeyError ('browser_name') could
occur during pytest_runtest_makereport.

# qase-pytest 6.1.13

## What's new

Resolved an issue in the pytest plugin where an AttributeError ('BookingForm' object has no attribute 'video') could
occur during pytest_runtest_makereport.

# qase-pytest 6.1.12

## What's new

1. Removed unsupported `tags` decorator as our API does not support working with tags.
2. Fixed an issue where data was not passed correctly when using `author` and `muted` decorators.

# qase-pytest 6.1.11

## What's new

Fixed issues with using `pytest.xfail` and the `skipif` mark:

1. Custom statuses did not work when using `pytest.xfail` within the test body.
2. The status was incorrect when using the `skipif` mark.

# qase-pytest 6.1.10

## What's new

The ability to override statuses for tests marked with the `xfail` marker has been added. By default, failed tests are
assigned the `skipped` status, and passed tests are assigned the `passed` status. Custom statuses can be specified by
providing the slug of the desired status in the configuration. Configuration values can be set via `qase.config.json` or
environment variables:

- `QASE_PYTEST_XFAIL_STATUS_XFAIL`
- `QASE_PYTEST_XFAIL_STATUS_XPASS`

```diff
{ ...,
  "framework": {
    "pytest": {
      "captureLogs": true,
      "xfailStatus": {
        "xfail": "skipped",
        "xpass": "passed"
      }
    }
  }
}
```

# qase-pytest 6.1.9

## What's new

Fixed an issue with parameters:

```log
INTERNALERROR>   File "/venv/lib/python3.9/site-packages/qase/pytest/plugin.py", line 331, in _set_params
INTERNALERROR>     value = str(ids[i])
INTERNALERROR> IndexError: list index out of range
```

# qase-pytest 6.1.8

## What's new

Fixed an issue with suites [#296]

# qase-pytest 6.1.7

## What's new

Support new version of qase-python-commons

# qase-pytest 6.1.6

## What's new

Fixed an issue with the handling video and trace recording for Playwright tests. If a test was part of a class, the
video
and trace were not attached to the test result.

# qase-pytest 6.1.5

## What's new

Improved the handling of videos and traces for Playwright tests.
You don't need to create a `conftest.py` file anymore. The video and trace will be attached to the test result
automatically.
You can configure the video and trace recording using the following parameters:

- `--video on` - add a video to each test
- `--video retain-on-failure` - add a video to each filed test
- `--tracing on` - add a trace to each test
- `--tracing retain-on-failure` - add a trace to each filed test
- `--output` - the directory where the video and trace will be saved. By default, the video and trace will be saved in
  the `test-results` directory.

# qase-pytest 6.1.4

## What's new

Improve handling parameters in the `pytest.mark.parametrize` decorator.
If you specify the `ids` parameter, the reporter will use it as value of parameter in the test case.

```python
@pytest.mark.parametrize("enter", [enter_from_meta, enter_from_expedition, enter_from_news],
                         ids=["enter_from_meta", "enter_from_expedition", "enter_from_news"])
def test_enter(enter):
    enter()
```

# qase-pytest 6.1.3

## What's new

If a video is attached to the result, it will be added as an attachment.
You can configure this functionality using the "video" parameter:

- `--video on` - add a video to each test
- `--video retain-on-failure` - add a video to each filed test

# qase-pytest 6.1.2

## What's new

Fixed an issue with the `pytest-xdist` that caused the tests to be run in parallel and completed the test run before the
results were uploaded to Qase.

# qase-pytest 6.1.1

## What's new

Minor release that includes all changes from beta versions 6.1.1b.

# qase-pytest 6.1.1b5

## What's new

Fixed an issue with `network` profiler.

# qase-pytest 6.1.1b4

## What's new

Fixed an issue with parameters like this:

```python
@pytest.mark.parametrize(argnames="foo", argvalues=["bar", "baz"])
```  

The error was:

```log
INTERNALERROR> File "/usr/local/lib/python3.12/site-packages/qase/pytest/plugin.py", line 79, in pytest_collection_modifyitems
INTERNALERROR> param_name, values = mark.args
INTERNALERROR> ^^^^^^^^^^^^^^^^^^
INTERNALERROR> ValueError: not enough values to unpack (expected 2, got 0)
```

# qase-pytest 6.1.1b3

## What's new

Fix an issue with the video recording option when the test fails:

```log
INTERNALERROR>     video = item.funcargs['page'].video
INTERNALERROR>             ~~~~~~~~~~~~~^^^^^^^^
INTERNALERROR> KeyError: 'page'
```

# qase-pytest 6.1.1b2

## What's new

If the video recording option is enabled and the test fails, the video will be attached to the test result when using
Playwright.

For configuration, you should create a `conftest.py` file in the root of your project and add the following code:

```python
import pytest


# Configure Playwright to record video for all tests
@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "record_video_dir": "./videos",  # Directory where videos will be saved
        "record_video_size": {"width": 1280, "height": 720}  # Video resolution
    }
```

# qase-pytest 6.1.1b1

## What's new

Support `pytest-rerunfailures` plugin. This plugin allows you to rerun failed tests.
Each test run will be uploaded as a separate result in Qase.

# qase-pytest 6.1.0

## What's new

Minor release that includes all changes from beta versions 6.1.0b.
And also added support for group parameters.

# qase-pytest 6.1.0b4

## What's new

- Exclude the default parameters that are added by additional libraries and start with `__pytest`
- If you use the `testops` mode and specify a plan ID then the reporter will run the tests specified in the test plan
  based on their IDs.

# qase-pytest 6.1.0b3

## What's new

Fixed an issue then `qase-pytest-capture-logs` parameter did not set correct value.

# qase-pytest 6.1.0b2

## What's new

Fixed the following issues:

- issue with `qase-pytest-capture-logs` parameter [#234].
  When using the "qase-pytest-capture-logs" parameter, an error occurred:
  `pytest: error: unrecognized arguments: --qase-pytest-capture-logs=true`

- issue with `qase-testops-batch-size` parameter [#235].
  When using the "qase-testops-batch-size" parameter, an error occurred:
  `TypeError: '>' not supported between instances of 'str' and 'int'`

# qase-pytest 6.1.0b1

## What's new

Implemented a method that constructs a signature for each test result.
It takes the file path, suites, qase IDs, and parameters.

# qase-pytest 6.0.3

## What's new

Fixed the issue where the suite specified in the decorator was not displayed. Fix [#231]

# qase-pytest 6.0.2

## What's new

Fixed the issue [#226]:

```log
TypeError: unsupported operand type(s) for +: 'NoneType' and 'str'
```

# qase-pytest 6.0.1

## What's new

Changed the name of the complete test run parameter for CLI arguments. Fix [#160]

# qase-pytest 6.0.0

## What's new

The first release in the 6.0.x series of the Pytest reporter.

# qase-pytest 6.0.0b2

## What's new

Turn off the sleep profiler until the test data collection is completed.
Now the profilers will turn off after the test is completed.
