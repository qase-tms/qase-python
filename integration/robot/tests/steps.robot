*** Settings ***
Documentation    Step tracking tests

*** Test Cases ***
Test With Multiple Steps
    [Tags]    Q-301
    Open Application
    Perform Action
    Verify Result

Test With Failing Step
    [Tags]    Q-302
    Open Application
    Trigger Failure

*** Keywords ***
Open Application
    Log    Application opened

Perform Action
    Log    Action performed

Verify Result
    Should Be True    ${TRUE}

Trigger Failure
    Should Be True    ${FALSE}    Step failure
