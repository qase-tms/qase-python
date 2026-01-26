# Multi-Project Support in Behave

Qase Behave Reporter supports sending test results to multiple Qase projects simultaneously. This feature allows you to report the same test execution to different projects with different test case IDs, which is useful when:

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

## Using `@qase.project_id.PROJECT_CODE:IDS` Tags

In Behave, you use tags to specify multi-project mappings. The format is `@qase.project_id.PROJECT_CODE:IDS` where `PROJECT_CODE` is the project code and `IDS` is a comma-separated list of test case IDs.

### Basic Usage

```gherkin
Feature: Example tests

  # Single project with single ID
  @qase.project_id.PROJ1:123
  Scenario: Example test with single ID
    Given I have a simple test
    When I run it
    Then it should pass

  # Single project with multiple IDs
  @qase.project_id.PROJ1:123,124
  Scenario: Example test with multiple IDs
    Given I have a simple test
    When I run it
    Then it should pass
```

### Multiple Projects

You can add multiple `@qase.project_id` tags to send results to multiple projects:

```gherkin
Feature: Example tests

  # Multiple projects, each with single ID
  @qase.project_id.PROJ1:123
  @qase.project_id.PROJ2:456
  Scenario: Example test for multiple projects
    Given I have a simple test
    When I run it
    Then it should pass

  # Multiple projects, each with multiple IDs
  @qase.project_id.PROJ1:123,124
  @qase.project_id.PROJ2:456,457
  Scenario: Complex multi-project test
    Given I have a simple test
    When I run it
    Then it should pass
```

### Combining with Other Tags

You can combine `@qase.project_id` tags with other Qase tags:

```gherkin
Feature: User authentication

  @qase.project_id.PROJ1:123
  @qase.fields:{"description":"User_login_test","severity":"critical"}
  @qase.suite:Authentication
  Scenario: User login test
    Given I am on the login page
    When I enter valid credentials
    Then I should be logged in
```

### Scenarios Without Project Mapping

If a scenario doesn't have any `@qase.project_id` tags, it will be sent to the `default_project` specified in your configuration:

```gherkin
Feature: Example tests

  Scenario: Test without project ID
    Given I have a simple test
    When I run it
    Then it should pass
```

If `default_project` is not specified, the first project from the `projects` array will be used.

## Feature-Level Tags

You can apply project ID tags at the Feature level, and all scenarios in that feature will inherit the mapping:

```gherkin
@qase.project_id.PROJ1:100
Feature: User management

  Scenario: Create user
    Given I am logged in
    When I create a new user
    Then the user should be created

  Scenario: Delete user
    Given I am logged in
    When I delete a user
    Then the user should be deleted
```

You can override the feature-level mapping for specific scenarios:

```gherkin
@qase.project_id.PROJ1:100
Feature: User management

  Scenario: Create user
    Given I am logged in
    When I create a new user
    Then the user should be created

  @qase.project_id.PROJ2:200
  Scenario: Delete user
    Given I am logged in
    When I delete a user
    Then the user should be deleted
```

## Tag Format Details

The tag format is case-sensitive and follows this pattern:

* Format: `@qase.project_id.PROJECT_CODE:ID1,ID2,ID3`
* `PROJECT_CODE`: Must match exactly with the project code in your configuration
* `IDS`: Comma-separated list of integers (no spaces around commas)
* Multiple tags can be used for multiple projects

Examples:

```gherkin
# Valid formats
@qase.project_id.PROJ1:123
@qase.project_id.PROJ1:123,124,125
@qase.project_id.PROJ1:123 @qase.project_id.PROJ2:456

# Invalid formats (will be ignored)
@qase.project_id.proj1:123  # Wrong case
@qase.project_id.PROJ1: 123  # Space after colon
@qase.project_id.PROJ1:123, 124  # Space in ID list
```

## Important Notes

1. **Project Codes Must Match**: The project codes used in tags must exactly match the codes specified in your `testops_multi.projects` configuration.

2. **Test Case IDs**: Each project can have different test case IDs for the same scenario. This allows you to maintain separate test case tracking in different projects.

3. **Test Run Creation**: Each project will have its own test run created (or use an existing run if `run.id` is specified in the project configuration).

4. **Results Distribution**: Test results are sent to all specified projects simultaneously. If a scenario fails, the failure will be reported to all projects.

5. **Default Project**: Scenarios without explicit project mapping will be sent to the `default_project`. If no `default_project` is specified, the first project in the configuration will be used.

6. **Mode Requirement**: You must set `mode` to `testops_multi` in your configuration file. Using `testops` mode will not work with `@qase.project_id` tags.

7. **Tag Parsing**: Tags are case-insensitive for the `qase.project_id` part, but the project code itself is case-sensitive.

## Examples

See the [multi-project examples](../../../examples/multiproject/behave/) directory for complete working examples.

## Troubleshooting

### Test results not appearing in projects

* Verify that `mode` is set to `testops_multi` in your `qase.config.json`
* Check that project codes in tags match exactly (case-sensitive) with configuration
* Ensure all projects are properly configured in `testops_multi.projects`
* Check debug logs for any errors during test run creation
* Verify tag format is correct (no spaces, proper comma separation)

### Scenarios sent to wrong project

* Verify the `default_project` setting if scenarios don't have explicit project mapping
* Check that project codes are case-sensitive and match exactly
* Review feature-level tags that might be affecting scenario mapping

### Multiple test runs created

* This is expected behavior - each project gets its own test run
* To use existing runs, specify `run.id` in each project's configuration

### Tag not recognized

* Ensure the tag starts with `@qase.project_id.` (case-insensitive)
* Check that there are no spaces in the tag
* Verify the colon (`:`) is used correctly to separate project code from IDs
* Ensure IDs are comma-separated without spaces
