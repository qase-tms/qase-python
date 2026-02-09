# Multi-Project Examples

Examples for reporting test results to multiple Qase projects simultaneously using `mode: testops_multi`.

## Overview

The multi-project feature allows you to send test results to multiple Qase projects with different test case IDs for each project. This is useful when:

- You need to report the same test to different projects
- Different projects track the same functionality with different test case IDs
- You want to maintain separate test runs for different environments or teams

## Frameworks

| Framework | Directory | Annotation Syntax |
|-----------|-----------|-------------------|
| Pytest | [pytest/](./pytest/) | `@qase.project_id("CODE", 1)` |
| Behave | [behave/](./behave/) | `@qase.project_id.CODE:1` |
| Robot Framework | [robot/](./robot/) | `Q-PROJECT.CODE-1` |
| Tavern | [tavern/](./tavern/) | `QaseProjectID.CODE=1` |

## Configuration

All examples use `qase.config.json` with `mode: testops_multi`:

```json
{
  "mode": "testops_multi",
  "testops": {
    "api": {
      "token": "<token>",
      "host": "qase.io"
    }
  },
  "testops_multi": {
    "default_project": "DEMO1",
    "projects": [
      {
        "code": "DEMO1",
        "run": {
          "title": "DEMO1 Multi-Project Run",
          "description": "Test run for DEMO1 project",
          "complete": true
        },
        "environment": "staging"
      },
      {
        "code": "DEMO2",
        "run": {
          "title": "DEMO2 Multi-Project Run",
          "description": "Test run for DEMO2 project",
          "complete": true
        },
        "environment": "production"
      }
    ]
  }
}
```

## Quick Start

1. Install the reporter package:
   ```bash
   pip install qase-pytest  # or qase-behave, qase-robotframework, qase-tavern
   ```

2. Navigate to the example directory:
   ```bash
   cd examples/multiproject/pytest
   ```

3. Update `qase.config.json`:
   - Replace `<token>` with your API token
   - Update project codes to match your Qase projects

4. Run the tests:
   ```bash
   # Pytest
   pytest tests/

   # Behave
   cd ../behave
   behave --format=qase.behave.formatter:QaseFormatter

   # Robot Framework
   cd ../robot
   robot --listener qase.robotframework.Listener tests/

   # Tavern
   cd ../tavern
   pytest
   ```

## Annotation Examples

### Single Project with Single ID

**Pytest:**
```python
@qase.project_id("DEMO1", 1)
def test_example():
    assert True
```

**Behave:**
```gherkin
@qase.project_id.DEMO1:1
Scenario: Example test
```

**Robot Framework:**
```robotframework
Test Case
    [Tags]    Q-PROJECT.DEMO1-1
```

**Tavern:**
```yaml
test_name: QaseProjectID.DEMO1=1 Example test
```

### Single Project with Multiple IDs

**Pytest:**
```python
@qase.project_id("DEMO1", [1, 2, 3])
def test_example():
    assert True
```

**Behave:**
```gherkin
@qase.project_id.DEMO1:1,2,3
Scenario: Example test
```

**Robot Framework:**
```robotframework
Test Case
    [Tags]    Q-PROJECT.DEMO1-1,2,3
```

**Tavern:**
```yaml
test_name: QaseProjectID.DEMO1=1,2,3 Example test
```

### Multiple Projects

**Pytest:**
```python
@qase.project_id("DEMO1", 1)
@qase.project_id("DEMO2", 10)
def test_example():
    assert True
```

**Behave:**
```gherkin
@qase.project_id.DEMO1:1 @qase.project_id.DEMO2:10
Scenario: Example test
```

**Robot Framework:**
```robotframework
Test Case
    [Tags]    Q-PROJECT.DEMO1-1    Q-PROJECT.DEMO2-10
```

**Tavern:**
```yaml
test_name: QaseProjectID.DEMO1=1 QaseProjectID.DEMO2=10 Example test
```

## Default Project

Tests without explicit project mapping are sent to `default_project`:

```python
# No @qase.project_id decorator
# This test goes to DEMO1 (default_project)
def test_without_project():
    assert True
```

## What to Expect

When you run the examples:

1. **Separate test runs** are created in each configured project
2. **Test results** are routed to the appropriate project based on annotations
3. **Tests without annotations** go to the `default_project`
4. **Each project** gets its own run with configured title and description

## Documentation

- [Multi-Project Guide (Pytest)](../../qase-pytest/docs/MULTI_PROJECT.md)
- [Multi-Project Guide (Behave)](../../qase-behave/docs/MULTI_PROJECT.md)
- [Multi-Project Guide (Robot Framework)](../../qase-robotframework/docs/MULTI_PROJECT.md)
- [Multi-Project Guide (Tavern)](../../qase-tavern/docs/MULTI_PROJECT.md)
- [Configuration Reference](../../qase-python-commons/README.md)
