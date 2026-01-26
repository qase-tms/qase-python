*** Settings ***
Library   steps.py

*** Test Cases ***

Test without metadata success
    Step 01
    Step 02
    Passed step

Test without metadata failed
    Step 01
    Step 02
    Failed Step


Test with QaseID success
    [Tags]     Q-10
    Step 01
    Step 02
    Passed step


Test with QaseID failed
    [Tags]     Q-11
    Step 01
    Step 02
    Failed Step


Ignored test success
    [Tags]     qase.ignore
    Step 01
    Step 02
    Passed step


Ignored test failed
    [Tags]     qase.ignore
    Step 01
    Step 02
    Failed Step


Test with fields success
    [Tags]     qase.fields:{ "preconditions": "Create object", "description": "It is simple test" }
    Step 01
    Step 02
    Passed step


Test with fields failed
    [Tags]     qase.fields:{ "preconditions": "Create object", "description": "It is simple test" }
    Step 01
    Step 02
    Failed Step


Test with all metadata success
    [Tags]     Q-12      qase.fields:{ "preconditions": "Create object", "description": "It is simple test" }
    Step 01
    Step 02
    Passed step


Test with all metadata failed
    [Tags]     Q-13      qase.fields:{ "preconditions": "Create object", "description": "It is simple test" }
    Step 01
    Step 02
    Failed Step
