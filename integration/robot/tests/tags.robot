*** Settings ***
Documentation    Tags tests

*** Test Cases ***
Test With Single Tag
    [Documentation]    Test with one tag
    [Tags]    Q-901    qase.tags:smoke
    Should Be True    ${TRUE}

Test With Multiple Tags
    [Documentation]    Test with multiple tags
    [Tags]    Q-902    qase.tags:smoke,regression,api
    Should Be True    ${TRUE}
