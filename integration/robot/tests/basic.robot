*** Settings ***
Documentation    Basic pass/fail/skip tests

*** Test Cases ***
Simple Passing Test
    [Tags]    Q-101
    Should Be True    ${TRUE}

Simple Failing Test
    [Tags]    Q-102
    Should Be True    ${FALSE}    Intentional failure

Skipped Test
    [Tags]    Q-103
    Skip    Skipped for integration testing
