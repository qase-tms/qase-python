*** Settings ***
Documentation    Field metadata tests

*** Test Cases ***
Test With Severity Blocker
    [Tags]    Q-201    qase.fields:{"severity":"blocker"}
    Should Be True    ${TRUE}

Test With Priority High
    [Tags]    Q-202    qase.fields:{"priority":"high"}
    Should Be True    ${TRUE}

Test With Layer E2E
    [Tags]    Q-203    qase.fields:{"layer":"e2e"}
    Should Be True    ${TRUE}

Test With Description
    [Tags]    Q-204    qase.fields:{"description":"Verifies description field"}
    Should Be True    ${TRUE}

Test With Multiple Fields
    [Tags]    Q-205    qase.fields:{"severity":"critical","priority":"high","layer":"api"}
    Should Be True    ${TRUE}
