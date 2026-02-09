# Robot Framework Examples

Examples demonstrating Qase Robot Framework Reporter features.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure credentials:
   ```bash
   export QASE_MODE=testops
   export QASE_TESTOPS_API_TOKEN=your_token
   export QASE_TESTOPS_PROJECT=your_project_code
   ```

   Or edit `qase.config.json` and replace `<token>` and `<project_code>`.

## Run Tests

```bash
# Run all tests
robot --listener qase.robotframework.Listener tests/

# Run specific test file
robot --listener qase.robotframework.Listener tests/simple.robot
```

## Examples

| File | Description |
|------|-------------|
| `simple.robot` | Basic tests with `Q-ID` tags, steps, and assertions |
| `parametrized.robot` | Data-driven tests with test templates |

## Code Examples

### Link to Test Case

```robotframework
*** Test Cases ***
Test With Qase ID
    [Tags]    Q-1
    Log    This test is linked to test case 1
    Should Be Equal    1    1

Test With Multiple IDs
    [Tags]    Q-1    Q-2    Q-3
    Log    Linked to multiple test cases
```

### Parametrized Tests

```robotframework
*** Test Cases ***    Expression    Expected
Addition              12 + 2 + 2    16
    [Tags]    Q-10
                      2 + -3        -1

Subtraction           12 - 2 - 2    8
    [Tags]    Q-11
                      2 - -3        5
```

### Working with Steps

Each keyword call is automatically reported as a step:

```robotframework
*** Test Cases ***
Test With Steps
    [Tags]    Q-5
    Step One           # Reported as step 1
    Step Two           # Reported as step 2
    Verify Result      # Reported as step 3

*** Keywords ***
Step One
    Log    Executing step one

Step Two
    Log    Executing step two

Verify Result
    Should Be True    ${TRUE}
```

## Documentation

- [Robot Framework Reporter README](../../../qase-robotframework/README.md)
- [Usage Guide](../../../qase-robotframework/docs/usage.md)
- [Configuration Reference](../../../qase-python-commons/README.md)
