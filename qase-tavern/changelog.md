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
