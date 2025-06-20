# [Qase TestOps](https://qase.io) Robot Framework Reporter

[![License](https://lxgaming.github.io/badges/License-Apache%202.0-blue.svg)](https://www.apache.org/licenses/LICENSE-2.0)

## Installation

```sh
pip install qase-robotframework
```

## Upgrade from 2.x to 3.x

The new version 3.x of the Robot Framework reporter has breaking changes.
To migrate from versions 2.x, follow the [upgrade guide](docs/UPGRADE.md).

## Configuration

Qase Robot Framework Reporter is configured in multiple ways:

- using a config file `qase.config.json`
- using environment variables

Environment variables override the values given in the config file.

Configuration options are described in the
[configuration reference](docs/CONFIGURATION.md).

### Example: qase.config.json

```json
{
  "mode": "testops",
  "fallback": "report",
  "debug": true,
  "testops": {
    "project": "YOUR_PROJECT_CODE",
    "api": {
      "token": "YOUR_API_TOKEN",
      "host": "qase.io"
    },
    "run": {
      "title": "Test run title"
    },
    "batch": {
      "size": 100
    }
  },
  "report": {
    "driver": "local",
    "connection": {
      "local": {
        "path": "./build/qase-report",
        "format": "json"
      }
    }
  },
  "environment": "local"
}
```

## Usage

For detailed instructions on using annotations and methods, refer to [Usage](docs/usage.md).

### Link tests with test cases in Qase TestOps

To link the automated tests with the test cases in Qase TestOps, use the tags in form like
`Q-<case id without project code>`.
Example:

```robotframework
*** Test Cases ***
Push button
    [Tags]  q-2
    Push button    1
    Result should be    1

Push multiple buttons
    [Tags]  Q-3
    Push button    1
    Push button    2
    Result should be    12
```

```robotframework
*** Test Cases ***    Expression    Expected
Addition              12 + 2 + 2    16
                      2 + -3        -1
    [Tags]   Q-7

Subtraction           12 - 2 - 2    8
                      2 - -3        5
    [Tags]   Q-8
```

### Working with steps

Listener supports reporting steps results:

Example:

```robotframework
Quick Get A JSON Body Test                                                  ## Test case: "Quick Get A JSON Body Test"
    [Tags]  Q-3
    ${response}=    GET  https://jsonplaceholder.typicode.com/posts/1       ## 1-st step - "GET"
    Should Be Equal As Strings    1  ${response.json()}[id]                 ## 2-nd step - "Should Be Equal As Strings"

Initializing the test case                                                  ## Test case: "Initializing the test case"
    [Tags]  q-4
    Set To Dictionary    ${info}   field1=A sample string                   ## 1-st step - "Set To Dictionary"
```

### Working with parameters

Listener supports reporting parameters:

Example:

```robotframework
*** Variables ***
${var1}            1
${var2}            1
${var3}            2

*** Test Cases ***
Simple test
    [Arguments]    ${var1}    ${var2}   ${var3}
    [Tags]     qase.params:[var1, var2]
    Should Be Equal As Numbers    ${var1}    ${var2}
    Should Be Equal As Numbers    ${var3}    ${var3} 
```

Only `var1` and `var2` will be sent to Qase.

### Execution:

```
robot --listener qase.robotframework.Listener someTest.robot
```
