*** Settings ***
Documentation    Multiple QaseIds test

*** Test Cases ***
Test Linked To Multiple Qase Test Cases
    [Tags]    Q-501    Q-502
    Should Be True    ${TRUE}
