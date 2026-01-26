# Multi-Project Support in Tavern

Qase Tavern Reporter supports sending test results to multiple Qase projects simultaneously. This feature allows you to report the same test execution to different projects with different test case IDs, which is useful when:

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

## Using `QaseProjectID.PROJECT_CODE=IDS` in Test Names

In Tavern, you specify multi-project mappings directly in the test name using the format `QaseProjectID.PROJECT_CODE=IDS` where `PROJECT_CODE` is the project code and `IDS` is a comma-separated list of test case IDs.

### Basic Usage

```yaml
---
# Single project with single ID
test_name: QaseProjectID.PROJ1=123 Get user by ID

stages:
  - name: Get user
    request:
      url: https://api.example.com/users/1
      method: GET
    response:
      status_code: 200

---
# Single project with multiple IDs
test_name: QaseProjectID.PROJ1=123,124 Get user by ID

stages:
  - name: Get user
    request:
      url: https://api.example.com/users/1
      method: GET
    response:
      status_code: 200
```

### Multiple Projects

You can specify multiple `QaseProjectID` entries in the test name to send results to multiple projects:

```yaml
---
# Multiple projects, each with single ID
test_name: QaseProjectID.PROJ1=123 QaseProjectID.PROJ2=456 Get user by ID

stages:
  - name: Get user
    request:
      url: https://api.example.com/users/1
      method: GET
    response:
      status_code: 200

---
# Multiple projects, each with multiple IDs
test_name: QaseProjectID.PROJ1=123,124 QaseProjectID.PROJ2=456,457 Get user by ID

stages:
  - name: Get user
    request:
      url: https://api.example.com/users/1
      method: GET
    response:
      status_code: 200
```

### Combining with QaseID

You cannot use both `QaseID` and `QaseProjectID` in the same test name. When using multi-project mode, always use `QaseProjectID`:

```yaml
---
# Correct: Using QaseProjectID for multi-project
test_name: QaseProjectID.PROJ1=123 QaseProjectID.PROJ2=456 Get user by ID

stages:
  - name: Get user
    request:
      url: https://api.example.com/users/1
      method: GET
    response:
      status_code: 200

---
# Incorrect: Mixing QaseID and QaseProjectID (QaseID will be ignored)
test_name: QaseID=123 QaseProjectID.PROJ2=456 Get user by ID

stages:
  - name: Get user
    request:
      url: https://api.example.com/users/1
      method: GET
    response:
      status_code: 200
```

### Tests Without Project Mapping

If a test doesn't have any `QaseProjectID` in its name, it will be sent to the `default_project` specified in your configuration:

```yaml
---
test_name: Get user by ID

stages:
  - name: Get user
    request:
      url: https://api.example.com/users/1
      method: GET
    response:
      status_code: 200
```

If `default_project` is not specified, the first project from the `projects` array will be used.

## Test Name Format Details

The format is case-insensitive and follows this pattern:

* Format: `QaseProjectID.PROJECT_CODE=ID1,ID2,ID3`
* `PROJECT_CODE`: Must match exactly with the project code in your configuration (case-sensitive)
* `IDS`: Comma-separated list of integers (spaces around commas are allowed)
* Multiple `QaseProjectID` entries can be used for multiple projects
* The rest of the test name after `QaseProjectID` entries will be used as the test title

Examples:

```yaml
# Valid formats
test_name: QaseProjectID.PROJ1=123 Get user by ID
test_name: QaseProjectID.PROJ1=123,124,125 Get user by ID
test_name: QaseProjectID.PROJ1=123 QaseProjectID.PROJ2=456 Get user by ID
test_name: qaseprojectid.proj1=123 Get user by ID  # Case-insensitive

# Invalid formats (will be ignored or cause errors)
test_name: QaseProjectID.proj1=123 Get user by ID  # Wrong case for project code (if config has PROJ1)
test_name: QaseProjectID.PROJ1:123 Get user by ID  # Wrong separator (should be =, not :)
```

## Order of Extraction

The reporter extracts project IDs from the test name in the following order:

1. First, all `QaseProjectID.PROJECT_CODE=IDS` patterns are extracted
2. If no project IDs are found, `QaseID=IDS` is extracted (for single-project mode)
3. The remaining text after extraction is used as the test title

Example:

```yaml
---
test_name: QaseProjectID.PROJ1=123 QaseProjectID.PROJ2=456 Get user by ID
```

This will:
* Extract project mapping: `PROJ1` → `[123]`, `PROJ2` → `[456]`
* Use "Get user by ID" as the test title

## Important Notes

1. **Project Codes Must Match**: The project codes used in test names must exactly match the codes specified in your `testops_multi.projects` configuration (case-sensitive).

2. **Test Case IDs**: Each project can have different test case IDs for the same test. This allows you to maintain separate test case tracking in different projects.

3. **Test Run Creation**: Each project will have its own test run created (or use an existing run if `run.id` is specified in the project configuration).

4. **Results Distribution**: Test results are sent to all specified projects simultaneously. If a test fails, the failure will be reported to all projects.

5. **Default Project**: Tests without explicit project mapping will be sent to the `default_project`. If no `default_project` is specified, the first project in the configuration will be used.

6. **Mode Requirement**: You must set `mode` to `testops_multi` in your configuration file. Using `testops` mode will not work with `QaseProjectID` format.

7. **Name Parsing**: The `QaseProjectID` part is case-insensitive, but the project code itself is case-sensitive and must match your configuration exactly.

8. **Spaces**: Spaces around the `=` sign and commas are allowed and will be trimmed automatically.

9. **Legacy Format**: The old `QaseID=IDS` format will still work in single-project mode, but will not work in multi-project mode. Use `QaseProjectID.PROJECT_CODE=IDS` instead.

## Examples

See the [multi-project examples](../../../examples/multiproject/tavern/) directory for complete working examples.

## Troubleshooting

### Test results not appearing in projects

* Verify that `mode` is set to `testops_multi` in your `qase.config.json`
* Check that project codes in test names match exactly (case-sensitive) with configuration
* Ensure all projects are properly configured in `testops_multi.projects`
* Check debug logs for any errors during test run creation
* Verify test name format is correct (equals sign separator, proper comma separation)

### Tests sent to wrong project

* Verify the `default_project` setting if tests don't have explicit project mapping
* Check that project codes are case-sensitive and match exactly
* Review test names to ensure `QaseProjectID` format is correct

### Multiple test runs created

* This is expected behavior - each project gets its own test run
* To use existing runs, specify `run.id` in each project's configuration

### Project ID not recognized

* Ensure the format is `QaseProjectID.PROJECT_CODE=IDS` (case-insensitive for `QaseProjectID` part)
* Check that an equals sign (`=`) is used to separate project code from IDs (not colon)
* Verify project code matches exactly (case-sensitive) with configuration
* Ensure IDs are comma-separated

### Old QaseID format not working

* In `testops_multi` mode, you must use `QaseProjectID.PROJECT_CODE=IDS` format
* Old `QaseID=IDS` format will only work in single-project `testops` mode
* Migrate your test names to the new format for multi-project support

### Test title is empty or incorrect

* The test title is extracted from the remaining text after removing all `QaseProjectID` patterns
* Ensure there is descriptive text after the project ID specifications
* Example: `QaseProjectID.PROJ1=123 Get user by ID` → title will be "Get user by ID"
