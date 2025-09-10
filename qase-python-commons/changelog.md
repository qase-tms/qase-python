# qase-python-commons@3.5.7

## What's new

- Fixed an issue where step request data was not being set correctly.

# qase-python-commons@3.5.6

## What's new

- Added support for updating external link for a test run.

# qase-python-commons@3.5.5

## What's new

- Improved test failure status handling across all reporters
- Added support for `invalid` status to distinguish non-assertion errors from assertion failures
- Updated `Execution` and `StepExecution` models to support `invalid` status
- Updated `RunStats` to track `invalid` status count
- Enhanced status filtering documentation to include `invalid` status
- Assertion errors (AssertionError) now map to `failed` status
- Non-assertion errors (setup failures, exceptions, etc.) now map to `invalid` status

## Migration Guide

The new `invalid` status provides better distinction between:
- `failed`: Test failed due to assertion error (test logic issue)
- `invalid`: Test failed due to non-assertion error (infrastructure/setup issue)

This change affects all reporters (pytest, tavern, behave, robotframework) and provides more accurate test result reporting.

# qase-python-commons@3.5.4

## What's new

- Added support for filtering test results by status.

# qase-python-commons@3.5.3

## What's new

- Added support for test run configurations. You can now specify configurations when creating test runs.
- Configurations can be specified in `qase.config.json`, environment variables, or CLI parameters.
- Support for automatic creation of configurations if they don't exist (controlled by `createIfNotExists` option).
- Added new models: `ConfigurationValue` and `ConfigurationsConfig` for handling test run configurations.
- Added methods in `ApiV1Client` for getting, finding, and creating configurations via API.

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

# qase-python-commons@3.5.2

## What's new

- Fixed an issue where the test run wasn't being completed before the results were uploaded.

# qase-python-commons@3.5.1

## What's new

- Fixed an issue where the test run was being completed before the results were uploaded.

# qase-python-commons@3.5.0

## What's new

- Added support for test run tags.
- Added support for excluding parameters from test results.
- Added support for signature generation. Now, the signature is generated based on the testops ids, suites and parameters.

# qase-python-commons@3.4.4

## What's new

Fixed an issue with the usage of the `pytest.skip` method iside a step body.

# qase-python-commons@3.4.3

## What's new

Improved logging and fixed several issues.

# qase-python-commons@3.4.2

## What's new

Fixed an issue with parsing boolean values from file-based configuration.

# qase-python-commons@3.4.1

## What's new

Fixed an issue with enum serialization in models

# qase-python-commons@3.4.0

## What's new

- Updated API clients to the latest supported versions.
- Improved logic for handling multiple QaseID values in test results.
- Removed `useV2` configuration option. The reporter now always uses API v2 for sending results.

# qase-python-commons@3.3.2

## What's new

- Logging of host system details to improve debugging and traceability.  
- Output of installed packages in logs for better environment visibility.

# qase-python-commons@3.3.1

## What's new

- Implemented local time support for test run creation to improve time tracking.
- Enhanced handling of start and end times for tests and steps, ensuring greater accuracy in reporting.

# qase-python-commons@3.3.0

## What's new

Enabled support for assigning multiple IDs to a single test result, allowing better traceability across test cases.

# qase-python-commons@3.2.7

## What's new

Resolved an issue where the defect field in the configuration was ignored during test result submission.

# qase-python-commons@3.2.5

## What's new

Updated logger to write logs to a single file from multiple threads, ensuring better concurrency handling and
readability.

# qase-python-commons@3.2.4

## What's new

- Support for custom statuses of xfail-marked tests in pytest.
- Default statuses: `skipped` (failed xfail) and `passed` (successful xfail).
- Configuration values can be set via `qase.config.json` or environment variables:
  - `QASE_PYTEST_XFAIL_STATUS_XFAIL`
  - `QASE_PYTEST_XFAIL_STATUS_XPASS`

# qase-python-commons@3.2.3

## What's new

Updated the handling of Gherkin steps to concatenate `keyword` and `name` into the action field when they differ,
providing
a more descriptive step action.

# qase-python-commons@3.2.2

## What's new

Fixed an issue with the `upload_attachment` method:

```log
attached.extend(self._upload_attachment(project_code, attachment))
TypeError: 'NoneType' object is not iterable
```

# qase-python-commons@3.2.1

## What's new

Use the API v2 client by default. If you want to use the API v1 client, specify the `useV2` option in the config file or
the environment variable `QASE_TESTOPS_USEV2` as `False`.

# qase-python-commons@3.2.0

## What's new

Updated the `file` reporter and support new API v2 client

# qase-python-commons@3.1.9

## What's new

Added configuration for Playwright framework. You can specify the `video`, `trace` and `output` options.

# qase-python-commons@3.1.7

## What's new

Fixed an issue with the `upload_attachment` method:

```log
"attachments": [attach.hash for attach in attached],
AttributeError: 'list' object has no attribute 'hash'
```

# qase-python-commons@3.1.7

## What's new

Show a test run link in end of log.

# qase-python-commons@3.1.6

## What's new

Change logic for uploading attachments. Now, the `upload_attachment` method won't return an error if the file is not
found.

# qase-python-commons@3.1.5

## What's new

Support `author` field in the test case model.
You can specify author name or email in fields.

# qase-python-commons@3.1.4

## What's new

- Add `clear` method to set the runtime to the base state.
- Make the `network` profiler thread safe.

# qase-python-commons@3.1.3

## What's new

Fix an issue with logging. The logger didn't write logs to the file if the OS used special encoding.

# qase-python-commons@3.1.2

## What's new

Support `suite` field in the test case model.

# qase-python-commons@3.1.0

## What's new

Minor release that includes all changes from beta versions 3.1.0b*.
Also added support for group parameters.

# qase-python-commons@3.1.0b7

## What's new

Fixed the following issue:

```log
HTTPSConnectionPool(host='api.qase.io', port=443): Max retries exceeded with url: /v1/plan/DEMO/1 (Caused by SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: self-signed certificate in certificate chain (_ssl.c:1000)')))
```

# qase-python-commons@3.1.0b6

## What's new

Reporters didn't send information about fields, like `title`, `description`, etc, to the Qase.
Now, the reporters will send all the information about the test case to the Qase.

# qase-python-commons@3.1.0b4

## What's new

Show a link to the test result in the Qase when the test has failed.

# qase-python-commons@3.1.0b3

## What's new

Fixed the problem [#176] with bool parameters. The config manager didn't get values in uppercase.

# qase-python-commons@3.1.0b2

## What's new

Fixed the following issues:

```log
AttributeError: 'QaseConfig' object has no attribute 'validate_config'
```

```log
'Run' object has no attribute 'to_json'
```

# qase-python-commons@3.1.0b1

## What's new

1. Change config type from `dict` to `object`
    - Add new config models.
    - Update retrieving data from the config in all dependencies.

2. Add a new configuration option `rootSuite` to specify a root suite.
   This option is available in the config file and the `QASE_ROOT_SUITE` env variable.

# qase-python-commons@3.0.3

## What's new

Fix an issue with getting bool parameters from the config when the parameter's value is `False`

# qase-python-commons@3.0.2

## What's new

First release in the 3.0.x series of the commons package.

# qase-python-commons@3.0.2b9

## What's new

Fixed an issue causing "Errno 22" error on Windows:

```log
[Errno 22] Invalid argument: .\\logs\\_20240101_00:00:00
```

# qase-python-commons@3.0.2b8

## What's new

Fixed the following issues:

- Return a correct default value from the config if the value was not found.
- Mark the `Field` model as exported.
- Fix the problem where the test run is completed before the results are sent.

# qase-python-commons@3.0.2b7

## What's new

Fixed the following issue:

```log
Creating instance failed: OSError: [ Errno 22 ] Invalid argument: './logs\file.log'
```

# qase-python-commons@3.0.2b6

## What's new

Fixed the following issue:

```log
[ ERROR ] Taking listener 'qaseio.robotframework.Listener' into use failed: 
    Importing listener 'qaseio.robotframework.Listener' failed: 
       ModuleNotFoundError: No module named 'pkg_resources'
```

# qase-python-commons@3.0.2b5

## What's new

A number of improvements in the network profiler:

- Ignoring requests to `qase.io` host.
- Checking that attributes `body` and `headers` are in the request.
- Fixed ignoring response for the `urllib3` package.
- Added a creation step for redirected requests

# qase-python-commons@3.0.2b4

## What's new

The sleep profiler was turned off until the test data collection was completed.
Now the profilers will turn off after the test is completed.

# qase-python-commons@3.0.2b3

## What's new

Added support for API V2. Specify the `useV2` option in the config file or the environment variable `QASE_TESTOPS_USEV2`

# qase-python-commons@3.0.2b2

## What's new

Migrate from old `qaseio` client to new `qase-api-clinet` client.  
