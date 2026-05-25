*** Settings ***
Documentation    Tests exercising IF/ELSE IF/ELSE branches.
...              Used to verify that conditional steps carry correct
...              start_time / end_time / duration into Qase TestOps.
Library          Collections
Library          String

*** Test Cases ***

IF Branch Taken
    [Documentation]    The first IF branch executes; ELSE branch is skipped.
    [Tags]    Q-100
    ${value}=    Set Variable    yes
    IF    "${value}" == "yes"
        Log    Going through the IF branch
        Sleep    50ms
        Should Be Equal    ${value}    yes
    ELSE
        Log    This ELSE must remain skipped
        Sleep    200ms
    END

ELSE Branch Taken
    [Documentation]    IF condition is false; ELSE branch executes.
    [Tags]    Q-101
    ${value}=    Set Variable    no
    IF    "${value}" == "yes"
        Log    This IF must remain skipped
        Sleep    200ms
    ELSE
        Log    Going through the ELSE branch
        Sleep    100ms
        Should Be Equal    ${value}    no
    END

ELSE IF Chain Middle Branch
    [Documentation]    Three-way chain: middle ELSE IF branch executes.
    [Tags]    Q-102
    ${value}=    Set Variable    medium
    IF    "${value}" == "low"
        Log    Low branch (skipped)
        Sleep    150ms
    ELSE IF    "${value}" == "medium"
        Log    Middle branch executing
        Sleep    75ms
        Should Be Equal    ${value}    medium
    ELSE
        Log    High branch (skipped)
        Sleep    150ms
    END
