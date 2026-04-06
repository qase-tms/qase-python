*** Settings ***
Documentation    Parametrized tests

*** Test Cases ***
Addition 1 Plus 2
    [Tags]    Q-401
    Verify Addition    1    2    3

Addition 4 Plus 5
    [Tags]    Q-402
    Verify Addition    4    5    9

*** Keywords ***
Verify Addition
    [Arguments]    ${a}    ${b}    ${expected}
    ${result}=    Evaluate    ${a} + ${b}
    Should Be Equal As Integers    ${result}    ${expected}
