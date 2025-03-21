# qase-robotframework 3.3.1

## What's new

Resolved an issue where `execution.start time` could be set incorrectly, leading to validation errors.

# qase-robotframework 3.3.0

## What's new

Added support for specifying multiple test case IDs for a single automated test, improving test case association and
traceability.

```robotframework
Example Test
    [Documentation]    Example test
    [Tags]  q-10     Q-20
    ${result}=         subtraction  5   3
    Should Be Equal    ${result}    2
```

# qase-robotframework 3.2.4

## What's new

1. Fixed handling of test steps with the `Message` type to ensure proper processing.
2. Resolved an issue with attachment handling, enabling correct attachment uploads.

# qase-robotframework 3.2.3

## What's new

Fixed an issue with Pabot
Resolved an issue where test runs were sometimes duplicated or test executions failed to complete under certain
conditions.

# qase-robotframework 3.2.2

## What's new

Support `qase.params` tag. You can specify the params that you want to send to Qase.

```robotframework
*** Variables ***
${var1}            1
${var2}            1
${var3}            2

*** Test Cases ***
Simple test
    [Arguments]    ${var1}    ${var2}   ${var3}
    [Tags]     qase.params:[var1, var2]
    Should Be Equal As Numbers    ${var1}    ${var2}
    Should Be Equal As Numbers    ${var3}    ${var3} 
```

Only `var1` and `var2` will be sent to Qase.

# qase-robotframework 3.2.1

## What's new

Support new version of qase-python-commons

# qase-robotframework 3.2.0

## What's new

Minor release that includes all changes from beta versions 3.2.0b.

Support `pabot` library. If you use the `pabot` library to run tests in parallel, the reporter will send the results

# qase-robotframework 3.2.0b3

## What's new

Improve handling of nested steps in the Robot Framework listener.

For example, if the test has the following structure:

```robotframework
Formatted Return
    RETURN  ${value}
```

Previously, the `RETURN` keyword was presented as `RETURN` in the Qase test run.
Now, the keyword is presented as `RETURN  ${value}`.

# qase-robotframework 3.2.0b2

## What's new

Fix an issue with nested steps in the Robot Framework listener.

# qase-robotframework 3.2.0b1

## What's new

- Migrate the listener to the `ROBOT_LISTENER_API_VERSION` version 3.
- Support a selective execution of tests by Qase ID.
  If the plan id is specified, the reporter will send the results only for the tests that are in the plan.

# qase-robotframework 3.1.2

## What's new

Support `qase.fields` tag. You can specify the fields that you want to send to Qase.

```robotframework
Simple test
    [Tags]     qase.fields:{ "suite": "my suite", "description": "It is simple test" }
    Should Be Equal As Numbers    1    1
```

# qase-robotframework 3.1.1

## What's new

Minor release that includes all changes from beta versions 3.1.1b.

Support `qase.ignore` tag. If the test has the `qase.ignore` tag, the reporter will not send the result to Qase.

```robotframework
Simple test
    [Tags]     qase.ignore
    Should Be Equal As Numbers    1    1
```

# qase-robotframework 3.1.1b2

## What's new

Fixed the issue:

```log
Calling method 'end_test' of listener 'qase.robotframework.Listener' failed: IndexError: list index out of range
```

# qase-robotframework 3.1.1b1

## What's new

Add support `robotframework-tidy` to the reporter.
The reporter will ignore `IF`, `ELSE IF`, `ELSE`, and `END` keywords.

# qase-robotframework 3.1.0

## What's new

Minor release that includes all changes from beta versions 3.1.0b.

# qase-robotframework 3.1.0b3

## What's new

Added the ability to attach attachments to step implementations.

```python
from qase.robotframework.method import qase


def step01(a: int, b: int):
    qase.attach("/some_path/file.xml")
    qase.attach((str.encode("This is a simple string attachment"), "text/plain", "simple.txt"))
    return str(a + b)
```

# qase-robotframework 3.1.0b1

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

Fixed an issue with unsupported step status. If the step is `skipped`, mark such a step as `blocked` in the Qase test
run.
