# qase-behave 1.0.2

## What's new

Added support for specifying multiple test case IDs for a single automated test, improving test case association and
traceability.

```gherkin
@qase.id:2,3,4
Scenario: Test with QaseID
```
# qase-behave 1.0.1

## What's new

Resolved an issue where tests marked with the `qase.ignore` tag were still being submitted to Qase.

# qase-behave 1.0.0

## What's new

The first release in the 1.0.x series of the Behave reporter.
