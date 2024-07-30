# qase-pytest 3.1.0b1

## What's new

Implemented a method that constructs a signature for each test result.
It takes the file path, suites, qase IDs, and parameters.

# qase-robotframework@3.0.0

## What's new

The first release in the 3.0.x series of the Robot Framework reporter.

# qase-robotframework@3.0.0b4

## What's new

The reporter will now extract the Qase ID after ending the test, not before.

# qase-robotframework@3.0.0b3

## What's new

Fixed the issue:

```log
AttributeError: 'Result' object has no attribute 'case'
```

Renamed the internal package from `qaseio` to `qase`.

# qase-robotframework@3.0.0b2

## What's new

Fixed an issue with unsupported step status. If the step is `skipped`, mark such a step as `blocked` in the Qase test run.
