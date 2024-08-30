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
- If you use the `testops` mode and specify a plan ID then the reporter will run the tests specified in the test plan based on their IDs.

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
