# Multi-Project Support in Robot Framework

Qase Robot Framework Reporter supports sending test results to multiple Qase projects simultaneously. This feature allows you to report the same test execution to different projects with different test case IDs, which is useful when:

* You need to report the same test to different projects
* Different projects track the same functionality with different test case IDs
* You want to maintain separate test runs for different environments or teams

## Configuration

For detailed configuration options, refer to the [qase-python-commons README](../../qase-python-commons/README.md#multi-project-support).

### Basic Multi-Project Configuration

To enable multi-project support, set the mode to `testops_multi` in your `qase.config.json`:

```json
{
  "mode": "testops_multi",
  "testops": {
    "api": {
      "token": "<your_api_token>",
      "host": "qase.io"
    },
    "batch": {
      "size": 100
    }
  },
  "testops_multi": {
    "default_project": "PROJ1",
    "projects": [
      {
        "code": "PROJ1",
        "run": {
          "title": "PROJ1 Test Run",
          "description": "Test run for PROJ1 project",
          "complete": true
        },
        "environment": "staging"
      },
      {
        "code": "PROJ2",
        "run": {
          "title": "PROJ2 Test Run",
          "description": "Test run for PROJ2 project",
          "complete": true
        },
        "environment": "production"
      }
    ]
  }
}
```

## Using `Q-PROJECT.PROJECT_CODE-IDS` Tags

In Robot Framework, you use tags to specify multi-project mappings. The format is `Q-PROJECT.PROJECT_CODE-IDS` where `PROJECT_CODE` is the project code and `IDS` is a comma-separated list of test case IDs.

### Basic Usage

```robotframework
*** Test Cases ***
# Single project with single ID
Test with single project ID
    [Tags]    Q-PROJECT.PROJ1-123
    Step 01
    Step 02
    Passed step

# Single project with multiple IDs
Test with multiple IDs
    [Tags]    Q-PROJECT.PROJ1-123,124
    Step 01
    Step 02
    Passed step
```

### Multiple Projects

You can add multiple `Q-PROJECT` tags to send results to multiple projects:

```robotframework
*** Test Cases ***
# Multiple projects, each with single ID
Test for multiple projects
    [Tags]    Q-PROJECT.PROJ1-123    Q-PROJECT.PROJ2-456
    Step 01
    Step 02
    Passed step

# Multiple projects, each with multiple IDs
Complex multi-project test
    [Tags]    Q-PROJECT.PROJ1-123,124    Q-PROJECT.PROJ2-456,457
    Step 01
    Step 02
    Passed step
```

### Combining with Other Tags

You can combine `Q-PROJECT` tags with other Qase tags:

```robotframework
*** Test Cases ***
Test with project ID and fields
    [Tags]    Q-PROJECT.PROJ1-123    qase.fields:{"priority":"high","severity":"critical"}
    Step 01
    Step 02
    Passed step
```

### Tests Without Project Mapping

If a test doesn't have any `Q-PROJECT` tags, it will be sent to the `default_project` specified in your configuration:

```robotframework
*** Test Cases ***
Test without project ID
    Step 01
    Step 02
    Passed step
```

If `default_project` is not specified, the first project from the `projects` array will be used.

## Tag Format Details

The tag format is case-insensitive and follows this pattern:

* Format: `Q-PROJECT.PROJECT_CODE-ID1,ID2,ID3`
* `PROJECT_CODE`: Must match exactly with the project code in your configuration (case-sensitive)
* `IDS`: Comma-separated list of integers (spaces around commas are allowed)
* Multiple tags can be used for multiple projects

Examples:

```robotframework
# Valid formats
[Tags]    Q-PROJECT.PROJ1-123
[Tags]    Q-PROJECT.PROJ1-123,124,125
[Tags]    Q-PROJECT.PROJ1-123    Q-PROJECT.PROJ2-456
[Tags]    q-project.proj1-123    # Case-insensitive for Q-PROJECT part

# Invalid formats (will be ignored)
[Tags]    Q-PROJECT.proj1-123  # Wrong case for project code (if config has PROJ1)
[Tags]    Q-PROJECT.PROJ1:123  # Wrong separator (should be dash, not colon)
```

## Test Suites

You can apply project ID tags at the suite level using `[Tags]` in the Settings section:

```robotframework
*** Settings ***
[Tags]    Q-PROJECT.PROJ1-100

*** Test Cases ***
Test Case 1
    Step 01
    Passed step

Test Case 2
    Step 01
    Passed step
```

All test cases in the suite will inherit the project mapping. You can override it for specific test cases:

```robotframework
*** Settings ***
[Tags]    Q-PROJECT.PROJ1-100

*** Test Cases ***
Test Case 1
    Step 01
    Passed step

Test Case 2
    [Tags]    Q-PROJECT.PROJ2-200
    Step 01
    Passed step
```

## Working with Parameters

Multi-project support works with parametrized tests:

```robotframework
*** Test Cases ***
Parametrized test
    [Tags]    Q-PROJECT.PROJ1-8
    [Template]    Check Value
    1
    2
    3

Check Value
    [Arguments]    ${value}
    Should Be True    ${value} > 0
```

## Important Notes

1. **Project Codes Must Match**: The project codes used in tags must exactly match the codes specified in your `testops_multi.projects` configuration (case-sensitive).

2. **Test Case IDs**: Each project can have different test case IDs for the same test. This allows you to maintain separate test case tracking in different projects.

3. **Test Run Creation**: Each project will have its own test run created (or use an existing run if `run.id` is specified in the project configuration).

4. **Results Distribution**: Test results are sent to all specified projects simultaneously. If a test fails, the failure will be reported to all projects.

5. **Default Project**: Tests without explicit project mapping will be sent to the `default_project`. If no `default_project` is specified, the first project in the configuration will be used.

6. **Mode Requirement**: You must set `mode` to `testops_multi` in your configuration file. Using `testops` mode will not work with `Q-PROJECT` tags.

7. **Tag Parsing**: The `Q-PROJECT` part is case-insensitive, but the project code itself is case-sensitive and must match your configuration exactly.

8. **Legacy Tags**: The old `Q-{ID}` format (without project specification) will still work in single-project mode, but will not work in multi-project mode. Use `Q-PROJECT.PROJECT_CODE-IDS` instead.

## Examples

See the [multi-project examples](../../../examples/multiproject/robot/) directory for complete working examples.

## Troubleshooting

### Test results not appearing in projects

* Verify that `mode` is set to `testops_multi` in your `qase.config.json`
* Check that project codes in tags match exactly (case-sensitive) with configuration
* Ensure all projects are properly configured in `testops_multi.projects`
* Check debug logs for any errors during test run creation
* Verify tag format is correct (dash separator, proper comma separation)

### Tests sent to wrong project

* Verify the `default_project` setting if tests don't have explicit project mapping
* Check that project codes are case-sensitive and match exactly
* Review suite-level tags that might be affecting test case mapping

### Multiple test runs created

* This is expected behavior - each project gets its own test run
* To use existing runs, specify `run.id` in each project's configuration

### Tag not recognized

* Ensure the tag starts with `Q-PROJECT.` (case-insensitive)
* Check that a dash (`-`) is used to separate project code from IDs (not colon)
* Verify project code matches exactly (case-sensitive) with configuration
* Ensure IDs are comma-separated

### Old Q-{ID} tags not working

* In `testops_multi` mode, you must use `Q-PROJECT.PROJECT_CODE-IDS` format
* Old `Q-{ID}` tags will only work in single-project `testops` mode
* Migrate your tags to the new format for multi-project support
