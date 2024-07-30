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
