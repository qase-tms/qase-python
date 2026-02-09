# Qase Integration in Robot Framework

This guide provides comprehensive instructions for integrating Qase with Robot Framework.

> **Configuration:** For complete configuration reference including all available options, environment variables, and examples, see the [qase-python-commons README](../../qase-python-commons/README.md).

---

## Table of Contents

- [Adding QaseID](#adding-qaseid)
- [Adding Fields](#adding-fields)
- [Adding Parameters](#adding-parameters)
- [Ignoring Tests](#ignoring-tests)
- [Working with Steps](#working-with-steps)
- [Multi-Project Support](#multi-project-support)
- [Running Tests](#running-tests)
- [Complete Examples](#complete-examples)

---

## Adding QaseID

Link your tests to existing test cases in Qase using the `Q-{ID}` tag format.

### Single ID

```robotframework
*** Test Cases ***
User Can Log In
    [Tags]    Q-1
    Open Login Page
    Enter Valid Credentials
    Verify Dashboard Is Visible
```

### Multiple IDs

Link one test to multiple test cases:

```robotframework
*** Test Cases ***
Complete Purchase Flow
    [Tags]    Q-1    Q-2    Q-3
    Add Item To Cart
    Proceed To Checkout
    Complete Payment
```

### Case Insensitive

Both `Q-1` and `q-1` are valid:

```robotframework
*** Test Cases ***
Test With Lowercase Tag
    [Tags]    q-1
    Log    This works too
```

### Multi-Project Support

To send test results to multiple Qase projects simultaneously, see the [Multi-Project Support Guide](MULTI_PROJECT.md).

---

## Adding Fields

Add metadata to your tests using the `qase.fields` tag with JSON format.

### System Fields

| Field | Description | Example Values |
|-------|-------------|----------------|
| `description` | Test case description | Any text |
| `preconditions` | Test preconditions | Any text |
| `postconditions` | Test postconditions | Any text |
| `severity` | Test severity | `blocker`, `critical`, `major`, `normal`, `minor`, `trivial` |
| `priority` | Test priority | `high`, `medium`, `low` |
| `layer` | Test layer | `e2e`, `api`, `unit` |

### Example

```robotframework
*** Test Cases ***
Critical Purchase Flow
    [Tags]    Q-1    qase.fields:{"severity":"critical","priority":"high","layer":"e2e"}
    Add Item To Cart
    Complete Checkout
```

### With Documentation

Robot Framework's `[Documentation]` is automatically used as the test description:

```robotframework
*** Test Cases ***
User Registration
    [Documentation]    Verify new user can register with valid email
    [Tags]    Q-1    qase.fields:{"severity":"major","preconditions":"User not registered"}
    Open Registration Page
    Fill Registration Form
    Submit Form
    Verify Success Message
```

### Fields in Keywords

Fields can also be added to user keywords:

```robotframework
*** Keywords ***
Verify Critical Feature
    [Tags]    qase.fields:{"severity":"critical"}
    Log    Verifying critical feature
```

---

## Adding Parameters

Report specific variables as test parameters using the `qase.params` tag.

### Basic Usage

```robotframework
*** Variables ***
${USERNAME}    testuser
${PASSWORD}    testpass
${BROWSER}     chrome

*** Test Cases ***
Login Test
    [Tags]    Q-1    qase.params:[USERNAME, PASSWORD]
    Login With Credentials    ${USERNAME}    ${PASSWORD}
```

Only `USERNAME` and `PASSWORD` will be reported to Qase.

### Multiple Parameters

```robotframework
*** Variables ***
${ENV}         staging
${BROWSER}     chrome
${USER_TYPE}   admin

*** Test Cases ***
Cross-Browser Test
    [Tags]    Q-1    qase.params:[ENV, USER_TYPE]
    Set Environment    ${ENV}
    Login As    ${USER_TYPE}
    Run Test In Browser    ${BROWSER}
```

### Parameters in Keywords

```robotframework
*** Keywords ***
Check Module Status
    [Arguments]    ${module}
    [Tags]    qase.params:[module]    qase.fields:{"severity":"critical"}
    Log    Checking status of module: ${module}

*** Test Cases ***
Check BMS Status
    [Tags]    Q-20
    Check Module Status    BMS
```

---

## Ignoring Tests

Exclude tests from Qase reporting while still executing them:

```robotframework
*** Test Cases ***
Work In Progress
    [Tags]    qase.ignore
    Log    This test runs but is not reported
```

---

## Working with Steps

Robot Framework keywords are automatically reported as test steps.

### Basic Keywords as Steps

```robotframework
*** Test Cases ***
Login Flow
    [Tags]    Q-1
    Open Login Page           # Step 1
    Enter Username            # Step 2
    Enter Password            # Step 3
    Click Login Button        # Step 4
    Verify Dashboard          # Step 5
```

### Nested Keywords

```robotframework
*** Keywords ***
Complete Login
    Open Login Page
    Enter Credentials    ${USERNAME}    ${PASSWORD}
    Click Login Button

Enter Credentials
    [Arguments]    ${user}    ${pass}
    Input Text    id=username    ${user}
    Input Text    id=password    ${pass}

*** Test Cases ***
User Login
    [Tags]    Q-1
    Complete Login            # Parent step
    Verify Dashboard
```

### Custom Step Names

Use meaningful keyword names for better step reporting:

```robotframework
*** Keywords ***
User Navigates To Product Page
    Go To    ${BASE_URL}/products

User Adds Item To Cart
    Click Button    id=add-to-cart

User Proceeds To Checkout
    Click Button    id=checkout

*** Test Cases ***
Purchase Flow
    [Tags]    Q-1
    User Navigates To Product Page
    User Adds Item To Cart
    User Proceeds To Checkout
```

---

## Multi-Project Support

Send test results to multiple Qase projects using the `Q-PROJECT.CODE-IDS` tag format:

```robotframework
*** Test Cases ***
Shared Test
    [Tags]    Q-PROJECT.PROJ1-1,2    Q-PROJECT.PROJ2-10
    Log    This test is reported to both projects
```

For detailed configuration, examples, and troubleshooting, see the [Multi-Project Support Guide](MULTI_PROJECT.md).

---

## Running Tests

### Basic Execution

```sh
robot --listener qase.robotframework.Listener tests/
```

### With Environment Variables

```sh
export QASE_MODE=testops
export QASE_TESTOPS_PROJECT=PROJ
export QASE_TESTOPS_API_TOKEN=your_token
robot --listener qase.robotframework.Listener tests/
```

### With Robot Variables

```sh
robot --listener qase.robotframework.Listener \
    --variable QASE_MODE:testops \
    --variable QASE_TESTOPS_PROJECT:PROJ \
    --variable QASE_TESTOPS_API_TOKEN:your_token \
    tests/
```

### Run Specific Suite

```sh
robot --listener qase.robotframework.Listener tests/login.robot
```

### Run With Tags

```sh
robot --listener qase.robotframework.Listener --include smoke tests/
```

### Parallel Execution with Pabot

```sh
pabot --listener qase.robotframework.Listener tests/
```

### With Existing Test Run

```sh
robot --listener qase.robotframework.Listener \
    --variable QASE_TESTOPS_RUN_ID:123 \
    tests/
```

---

## Complete Examples

### Full Test Suite

```robotframework
*** Settings ***
Library    SeleniumLibrary
Library    Collections

*** Variables ***
${BASE_URL}     https://example.com
${BROWSER}      chrome
${USERNAME}     testuser
${PASSWORD}     testpass

*** Test Cases ***
User Registration
    [Documentation]    Verify new user can register successfully
    [Tags]    Q-1    qase.fields:{"severity":"critical","priority":"high","layer":"e2e"}
    [Setup]    Open Browser    ${BASE_URL}    ${BROWSER}
    Navigate To Registration Page
    Fill Registration Form    ${USERNAME}    ${PASSWORD}
    Submit Form
    Verify Registration Success
    [Teardown]    Close Browser

User Login With Valid Credentials
    [Documentation]    Verify registered user can login
    [Tags]    Q-2    qase.params:[USERNAME, PASSWORD]
    [Setup]    Open Browser    ${BASE_URL}    ${BROWSER}
    Navigate To Login Page
    Enter Credentials    ${USERNAME}    ${PASSWORD}
    Click Login Button
    Verify Dashboard Is Visible
    [Teardown]    Close Browser

User Login With Invalid Password
    [Documentation]    Verify error message for invalid password
    [Tags]    Q-3    qase.fields:{"severity":"major"}
    [Setup]    Open Browser    ${BASE_URL}    ${BROWSER}
    Navigate To Login Page
    Enter Credentials    ${USERNAME}    wrongpassword
    Click Login Button
    Verify Error Message Is Shown
    [Teardown]    Close Browser

Ignored Test
    [Tags]    qase.ignore
    Log    This test is not reported to Qase

*** Keywords ***
Navigate To Registration Page
    Go To    ${BASE_URL}/register

Navigate To Login Page
    Go To    ${BASE_URL}/login

Fill Registration Form
    [Arguments]    ${user}    ${pass}
    Input Text    id=username    ${user}
    Input Text    id=email       ${user}@example.com
    Input Text    id=password    ${pass}
    Input Text    id=confirm     ${pass}

Enter Credentials
    [Arguments]    ${user}    ${pass}
    Input Text    id=username    ${user}
    Input Text    id=password    ${pass}

Submit Form
    Click Button    id=submit

Click Login Button
    Click Button    id=login

Verify Registration Success
    Page Should Contain    Registration successful

Verify Dashboard Is Visible
    Page Should Contain Element    id=dashboard

Verify Error Message Is Shown
    Page Should Contain    Invalid credentials
```

### Example Project Structure

```
my-project/
├── qase.config.json
├── tests/
│   ├── login.robot
│   ├── checkout.robot
│   └── api/
│       └── users.robot
├── resources/
│   ├── keywords.robot
│   └── variables.robot
└── requirements.txt
```

---

## Troubleshooting

### Tests Not Appearing in Qase

1. Verify `mode` is set to `testops`
2. Check API token has write permissions
3. Verify project code is correct
4. Ensure listener is specified: `--listener qase.robotframework.Listener`

### Parameters Not Reporting

1. Verify variable names match exactly (case-sensitive)
2. Check `qase.params` syntax: `qase.params:[VAR1, VAR2]`
3. Ensure variables are defined

### Parallel Execution Issues

1. Use pabot instead of robot for parallel runs
2. Ensure each worker has access to configuration
3. Check for race conditions in shared resources

---

## See Also

- [Configuration Reference](../../qase-python-commons/README.md)
- [Multi-Project Support](MULTI_PROJECT.md)
- [Upgrade Guide](UPGRADE.md)
