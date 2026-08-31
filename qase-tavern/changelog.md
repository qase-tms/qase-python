# qase-tavern 4.0.0

## Breaking changes

- Failure status is now derived from the pytest phase (`call.when`) instead of guessed from the exception type. pytest-tavern raises its own `TestFailError` for a failing stage, never `AssertionError`, so under the old logic **every** call-phase failure was reported as `invalid` — real product/test failures never showed up as `failed`. `setup`/`teardown` failures (e.g. a broken pytest fixture used by a Tavern test) weren't processed at all and shipped with `status: null`; they're now reported as `invalid`, without ever overwriting an already-failed call-phase result. ([#511](https://github.com/qase-tms/qase-python/issues/511))

  | Failure phase | Old status (guessed from exception text) | New status (from pytest phase) |
  |---|---|---|
  | Test body (`call`) fails with what looks like an assertion (message contains `assert`/`should`/`equal`/...) | `failed` | `failed` |
  | Test body (`call`) fails with anything else (custom exception, timeout, `pytest.fail()`, framework error text) | `invalid` — wrong | `failed` |
  | Setup / before-hook fails | `invalid`, unless the exception's message happened to match an assertion keyword, in which case `failed` — inconsistent | `invalid` |
  | Teardown / after-hook fails, test body already passed | `passed` — wrong, hides the failure | `invalid` |
  | Teardown / after-hook fails, test body already failed | body's status kept, but the teardown message could silently overwrite the real failure's message/stacktrace | body's status and diagnostics are kept untouched — the real failure always wins |

  If your suite relies on the old behaviour, review any downstream logic (dashboards, defect linking, status filters) that branches on `invalid` vs `failed`.

# qase-tavern 3.1.0

## What's new

- Added support for test-level tags using the `QaseTags.tag1,tag2` prefix in test names.

# qase-tavern 3.0.0

## What's new

- Added support for multi-project reporting. You can now send test results to multiple Qase projects simultaneously. More information about multi-project reporting can be found in the [docs](docs/usage.md#multi-project-support).

# qase-tavern 2.0.5

## What's new

- Updated the `qase-python-commons` dependency to the latest version.

# qase-tavern 2.0.4

## What's new

- Added support for automatic public report link generation.

# qase-tavern 2.0.3

## Bug fixes

- Fixed filelock dependency compatibility issue with modern tox versions. Changed filelock requirement from `~=3.12.2` to `>=3.12.2` to support newer versions required by tox>=4.26.0 and tox-uv. This resolves dependency conflicts when using modern development tools.

# qase-tavern 2.0.2

## What's new

- Added support for logging configuration. More information about logging configuration can be found in the [docs](../qase-python-commons/docs/LOGGING.md).

# qase-tavern 2.0.1

## What's new

- Added support for status mapping. More information about status mapping can be found in the [docs](../qase-python-commons/docs/STATUS_MAPPING.md).

# qase-tavern 2.0.0

## What's new

- Unsupport Python 3.7 and 3.8. Support Python 3.9, 3.10, 3.11, 3.12, 3.13.
- Updated the `qase-python-commons` dependency to the latest version.

# qase-tavern 1.1.5

## What's new

- Added support for updating external link for a test run.
- Updated dependency on qase-python-commons to version 3.5.6.

# qase-tavern 1.1.4

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

# qase-tavern 1.1.3

## What's new

- Added support for filtering test results by status.

# qase-tavern 1.1.2

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

# qase-tavern 1.1.1

## What's new

- Added support for test run tags.
- Added support for excluding parameters from test results.
  
# qase-tavern 1.1.0

## What's new

- Updated core package to the latest supported versions.
- Improved logic for handling multiple QaseID values in test results.
- Removed `useV2` configuration option. The reporter now always uses API v2 for sending results.

# qase-tavern 1.0.3

## What's new

- Logging of host system details to improve debugging and traceability.  
- Output of installed packages in logs for better environment visibility.  

# qase-tavern 1.0.2

## What's new

Added support for specifying multiple test case IDs for a single automated test, improving test case association and
traceability.

```yaml
test_name: QaseID=2,3,4 Test with QaseID
stages:
  - name: Step 1
...
```

# qase-tavern 1.0.0

## What's new

The first release in the 1.0.x series of the Tavern reporter.
