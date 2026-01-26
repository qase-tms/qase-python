# Qase Integration in Robot Framework

This guide demonstrates how to integrate Qase with Robot Framework, providing instructions on how to add Qase IDs, fields, and other metadata to your test cases.

## Adding QaseID to a Test

To associate a QaseID with a test in Robot Framework, use the `Q-{ID}` tag format.

```robotframework
*** Test Cases ***
Test with QaseID
    [Tags]    Q-10
    Step 01
    Step 02
    Passed step

Test with multiple QaseIDs
    [Tags]    Q-11    Q-12
    Step 01
    Step 02
    Passed step
```

### Multi-Project Support

To send test results to multiple projects with different test case IDs, use the `Q-PROJECT.PROJECT_CODE-IDS` tag format:

```robotframework
*** Test Cases ***
# Single project with multiple IDs
Test with project IDs
    [Tags]    Q-PROJECT.PROJ1-123,124
    Step 01
    Step 02
    Passed step

# Multiple projects with different IDs
Test for multiple projects
    [Tags]    Q-PROJECT.PROJ1-123    Q-PROJECT.PROJ2-456
    Step 01
    Step 02
    Passed step

# Multiple projects with multiple IDs each
Complex multi-project test
    [Tags]    Q-PROJECT.PROJ1-123,124    Q-PROJECT.PROJ2-456,457
    Step 01
    Step 02
    Passed step
```

**Note:** When using `Q-PROJECT`, the test results will be sent to all specified projects. Make sure to configure `testops_multi` mode in your `qase.config.json` file.

---

## Adding Fields to a Test

The `qase.fields` tag allows you to add additional metadata to a test case using JSON format.

```robotframework
*** Test Cases ***
Test with fields
    [Tags]    qase.fields:{"priority": "high", "severity": "critical", "layer": "UI"}
    Step 01
    Step 02
    Passed step

Test with description and preconditions
    [Tags]    qase.fields:{"description": "User login test", "preconditions": "User is not logged in"}
    Step 01
    Step 02
    Passed step
```

### Available Fields

You can add any custom fields, but some common ones include:

- `description` - Description of the test case
- `preconditions` - Preconditions for the test case
- `postconditions` - Postconditions for the test case
- `severity` - Severity of the test case (e.g., `critical`, `major`)
- `priority` - Priority of the test case (e.g., `high`, `low`)
- `layer` - Test layer (e.g., `UI`, `API`)

---

## Adding Parameters to a Test

The `qase.params` tag allows you to specify which Robot Framework variables should be reported as parameters.

```robotframework
*** Variables ***
${username}    testuser
${password}    testpass
${browser}     chrome

*** Test Cases ***
Login Test
    [Tags]    qase.params:[username, password]
    Login with credentials    ${username}    ${password}
    Verify login successful

Browser Test
    [Tags]    qase.params:[browser]
    Open browser    ${browser}
    Navigate to page
    Close browser
```

### Adding Parameters and Fields to a User Keyword

The `qase.params` tag can also be used in user keywords to specify which Robot Framework variables should be reported as parameters.

```robotframework
*** Settings ***
Test Template    Check Status

*** Keywords ***
Check Status
    [Arguments]    ${module}     
    [Tags]    qase.params:[module]    qase.fields:{ "severity": "critical" }
    Log    Checking status of module: ${module}

*** Test Cases ***
Check Status of BMS
    [Tags]   Q-20     qase.fields:{ "preconditions": "Module BMS is connected", "description": "Flash firmware to BMS module and check status" }
    [Template]    Check Status
    BMS 

```

---

## Ignoring a Test in Qase

To exclude a test from being reported to Qase (while still executing the test), use the `qase.ignore` tag.

```robotframework
*** Test Cases ***
Ignored test
    [Tags]    qase.ignore
    Step 01
    Step 02
    Passed step
```

---

## Combining Multiple Tags

You can combine multiple Qase tags in a single test:

```robotframework
*** Test Cases ***
Complete test with all metadata
    [Tags]    Q-15    qase.fields:{"priority": "high", "severity": "critical"}    qase.params:[username, password]
    Step 01
    Step 02
    Passed step
```

---

## Test Documentation

Robot Framework automatically uses the test documentation as the test description in Qase:

```robotframework
*** Test Cases ***
User Login Test
    [Documentation]    Test user login functionality with valid credentials
    [Tags]    Q-20
    Step 01
    Step 02
    Passed step
```

---

## Advanced Configuration

### Parallel Execution

For parallel execution with pabot, the plugin automatically handles worker coordination:

```bash
pabot --listener qase.robotframework.Listener --variable QASE_TESTOPS_PROJECT:PROJECT_CODE --variable QASE_TESTOPS_API_TOKEN:YOUR_TOKEN tests/
```

---

## Examples

### Complete Test Suite Example

```robotframework
*** Settings ***
Library    SeleniumLibrary
Library    steps.py

*** Variables ***
${base_url}    https://example.com
${username}    testuser
${password}    testpass

*** Test Cases ***
User Registration Test
    [Documentation]    Test user registration with valid data
    [Tags]    Q-1    qase.fields:{"priority": "high", "severity": "critical", "layer": "UI"}
    [Setup]    Open browser    ${base_url}    chrome
    Navigate to registration page
    Fill registration form    ${username}    ${password}
    Submit registration form
    Verify registration successful
    [Teardown]    Close browser

User Login Test
    [Documentation]    Test user login with valid credentials
    [Tags]    Q-2    qase.params:[username, password]
    [Setup]    Open browser    ${base_url}    chrome
    Navigate to login page
    Fill login form    ${username}    ${password}
    Submit login form
    Verify login successful
    [Teardown]    Close browser

Ignored Test
    [Documentation]    This test is ignored in Qase
    [Tags]    qase.ignore
    Step 01
    Step 02
    Passed step

*** Keywords ***
Navigate to registration page
    Go to    ${base_url}/register

Fill registration form
    [Arguments]    ${username}    ${password}
    Input text    id=username    ${username}
    Input text    id=password    ${password}

Submit registration form
    Click button    id=submit

Verify registration successful
    Page should contain    Registration successful

Navigate to login page
    Go to    ${base_url}/login

Fill login form
    [Arguments]    ${username}    ${password}
    Input text    id=username    ${username}
    Input text    id=password    ${password}

Submit login form
    Click button    id=submit

Verify login successful
    Page should contain    Welcome
```

### Running Tests

```bash
# Basic run
robot --listener qase.robotframework.Listener --variable QASE_TESTOPS_PROJECT:MYPROJECT --variable QASE_TESTOPS_API_TOKEN:YOUR_TOKEN tests/

# With environment and plan
robot --listener qase.robotframework.Listener --variable QASE_TESTOPS_PROJECT:MYPROJECT --variable QASE_TESTOPS_API_TOKEN:YOUR_TOKEN --variable QASE_ENVIRONMENT:staging --variable QASE_TESTOPS_PLAN_ID:123 tests/

# With execution plan
robot --listener qase.robotframework.Listener --variable QASE_TESTOPS_PROJECT:MYPROJECT --variable QASE_TESTOPS_API_TOKEN:YOUR_TOKEN --variable QASE_EXECUTION_PLAN_PATH:plan.json tests/

# Parallel execution
pabot --listener qase.robotframework.Listener --variable QASE_TESTOPS_PROJECT:MYPROJECT --variable QASE_TESTOPS_API_TOKEN:YOUR_TOKEN tests/
```
