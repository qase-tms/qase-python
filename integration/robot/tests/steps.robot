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

Test With Single Tag
    [Documentation]    Test with one tag
    [Tags]    Q-901    qase.tags:smoke
    Should Be True    ${TRUE}

Test With Multiple Tags
    [Documentation]    Test with multiple tags
    [Tags]    Q-902    qase.tags:smoke,regression,api
    Should Be True    ${TRUE}

*** Keywords ***
Open Application
    Log    Application opened

Perform Action
    Log    Action performed

Verify Result
    Should Be True    ${TRUE}

Trigger Failure
    Should Be True    ${FALSE}    Step failure
