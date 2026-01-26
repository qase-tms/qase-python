*** Settings ***
Documentation    Multi-project tests for Robot Framework
Library          BuiltIn

*** Test Cases ***
Single Project Single ID
    [Tags]    Q-PROJECT.DEVX-1
    Log    This is a simple test for DEVX project
    Should Be Equal    2    2

Single Project Multiple IDs
    [Tags]    Q-PROJECT.DEVX-2,3
    Log    This test has multiple IDs for DEVX project
    ${result}=    Evaluate    1 + 1
    Should Be Equal    ${result}    2

Multiple Projects Single ID
    [Tags]    Q-PROJECT.DEVX-4    Q-PROJECT.DEMO-10
    Log    This test is for multiple projects
    Should Be Equal    hello    hello

Multiple Projects Multiple IDs
    [Tags]    Q-PROJECT.DEVX-5,6    Q-PROJECT.DEMO-11,12
    Log    This is a complex multi-project test
    ${result}=    Evaluate    2 * 3
    Should Be Equal    ${result}    6

Failed Test for DEVX
    [Tags]    Q-PROJECT.DEVX-7
    Log    This test will fail for DEVX project
    Should Be Equal    1    2    This test intentionally fails

Passed Test for DEMO
    [Tags]    Q-PROJECT.DEMO-13
    Log    This test will pass for DEMO project
    Should Be Equal    1    1

Test Without Any ID
    Log    This test has no ID and should be sent to first project (DEVX)
    Should Be Equal    1    1
