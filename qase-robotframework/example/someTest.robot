*** Settings ***
Library  RequestsLibrary
Library  Collections

*** Test Cases ***

Quick Get Request Test
    [Tags]  Q-1
    Create Session    google  http://www.google.com                         ## First step in Qase TMS
    ${response}=    GET  https://www.google.com                             ## Second step in Qase TMS

Quick Get Request With Parameters Test                                      ## ----------------------
    [Tags]  q-2
    Create Session    google  http://www.google.com                         ## First step in Qase TMS
    ${resp_google}=   GET On Session  google  /  expected_status=200        ## Second step in Qase TMS

    Should Be Equal As Strings          ${resp_google.reason}  OK           ## Third step in Qase TMS

Quick Get A JSON Body Test                                                  ## ----------------------
    [Tags]  Q-3
    ${response}=    GET  https://jsonplaceholder.typicode.com/posts/1       ## First step in Qase TMS
    Should Be Equal As Strings    1  ${response.json()}[id]                 ## Second step in Qase TMS

Initializing the test case                                                  ## ----------------------
    [Tags]  q-4
    Set To Dictionary    ${info}   field1=A sample string                   ## First step in Qase TMS

*** Variables ***
&{info}
