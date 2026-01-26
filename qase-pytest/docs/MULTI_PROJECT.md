# Multi-Project Support in Pytest

Qase Pytest Reporter supports sending test results to multiple Qase projects simultaneously. This feature allows you to report the same test execution to different projects with different test case IDs, which is useful when:

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

## Using `@qase.project_id()` Decorator

The `@qase.project_id()` decorator allows you to specify which project(s) a test should be reported to and which test case IDs to use for each project.

### Basic Usage

```python
from qase.pytest import qase

# Single project with single ID
@qase.project_id("PROJ1", 123)
def test_example():
    assert True

# Single project with multiple IDs
@qase.project_id("PROJ1", [123, 124])
def test_multiple_ids():
    assert True
```

### Multiple Projects

You can apply multiple `@qase.project_id()` decorators to send results to multiple projects:

```python
from qase.pytest import qase

# Multiple projects, each with single ID
@qase.project_id("PROJ1", 123)
@qase.project_id("PROJ2", 456)
def test_multiple_projects():
    assert True

# Multiple projects, each with multiple IDs
@qase.project_id("PROJ1", [123, 124])
@qase.project_id("PROJ2", [456, 457])
def test_complex_multi_project():
    assert True
```

### Combining with Other Decorators

You can combine `@qase.project_id()` with other Qase decorators:

```python
from qase.pytest import qase

@qase.project_id("PROJ1", 123)
@qase.title("User Login Test")
@qase.fields(
    ("severity", "critical"),
    ("priority", "high")
)
def test_login():
    assert True
```

### Tests Without Project Mapping

If a test doesn't have any `@qase.project_id()` decorator, it will be sent to the `default_project` specified in your configuration:

```python
def test_without_id():
    """This test will be sent to the default_project from config."""
    assert True
```

If `default_project` is not specified, the first project from the `projects` array will be used.

## Parametrized Tests

Multi-project support works with parametrized tests:

```python
import pytest
from qase.pytest import qase

@pytest.mark.parametrize("value", [1, 2, 3])
@qase.project_id("PROJ1", 8)
def test_parametrized(value):
    assert value > 0
```

Each parametrized test instance will be reported to the specified project with the same test case ID.

## Test Classes

You can apply `@qase.project_id()` to test classes:

```python
from qase.pytest import qase

@qase.project_id("PROJ1", 100)
class TestUserManagement:
    def test_create_user(self):
        assert True
    
    def test_delete_user(self):
        assert True
```

All test methods in the class will inherit the project mapping. You can override it for specific methods:

```python
from qase.pytest import qase

@qase.project_id("PROJ1", 100)
class TestUserManagement:
    def test_create_user(self):
        assert True
    
    @qase.project_id("PROJ2", 200)
    def test_delete_user(self):
        assert True
```

## Important Notes

1. **Project Codes Must Match**: The project codes used in `@qase.project_id()` must exactly match the codes specified in your `testops_multi.projects` configuration.

2. **Test Case IDs**: Each project can have different test case IDs for the same test. This allows you to maintain separate test case tracking in different projects.

3. **Test Run Creation**: Each project will have its own test run created (or use an existing run if `run.id` is specified in the project configuration).

4. **Results Distribution**: Test results are sent to all specified projects simultaneously. If a test fails, the failure will be reported to all projects.

5. **Default Project**: Tests without explicit project mapping will be sent to the `default_project`. If no `default_project` is specified, the first project in the configuration will be used.

6. **Mode Requirement**: You must set `mode` to `testops_multi` in your configuration file. Using `testops` mode will not work with `@qase.project_id()` decorators.

## Examples

See the [multi-project examples](../../../examples/multiproject/pytest/) directory for complete working examples.

## Troubleshooting

### Test results not appearing in projects

* Verify that `mode` is set to `testops_multi` in your `qase.config.json`
* Check that project codes in decorators match exactly with configuration
* Ensure all projects are properly configured in `testops_multi.projects`
* Check debug logs for any errors during test run creation

### Tests sent to wrong project

* Verify the `default_project` setting if tests don't have explicit project mapping
* Check that project codes are case-sensitive and match exactly

### Multiple test runs created

* This is expected behavior - each project gets its own test run
* To use existing runs, specify `run.id` in each project's configuration
