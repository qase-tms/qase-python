*** Settings ***
Library    steps.py

*** Variables ***
${var1}            1
${var2}            1
${var3}            2

*** Test Cases ***
Parametrized Test success
    [Tags]     qase.params:[var1, var2]
    Check numbers   ${var1}    ${var2}    ${var3}
    Passed Step

Parametrized Test failed
    [Tags]     qase.params:[var1, var2]
    Check numbers   ${var1}    ${var2}    ${var3}
    Failed Step


*** Keywords ***
Check numbers
    [Arguments]    ${var1}    ${var2}      ${var3}
    Should Be Equal As Numbers    ${var1}    ${var2}
    Should Be Equal As Numbers    ${var3}    ${var3}
