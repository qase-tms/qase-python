# Multi-Project Examples

This directory contains examples demonstrating how to use Qase TestOps with multiple projects.

## Overview

The multi-project feature allows you to send test results to multiple Qase projects simultaneously, with different test case IDs for each project. This is useful when:
- You need to report the same test to different projects
- Different projects track the same functionality with different test case IDs
- You want to maintain separate test runs for different environments or teams

## Projects Used in Examples

- **DEMO1**: Development/Staging project
- **DEMO2**: Demo/Production project

## Configuration

All examples use a `qase.config.json` configuration file with the following structure:

```json
{  
  "mode": "testops_multi",
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

## Running Examples

### Pytest

1. **Install packages in development mode** (required for local changes):
   ```bash
   cd qase-python
   pip install -e qase-python-commons
   pip install -e qase-pytest
   ```

   Or use the development requirements:
   ```bash
   cd examples/multiproject/pytest
   pip install -r requirements.dev.txt
   ```

2. Update the API token in `qase.config.json`

3. Run the tests:
   ```bash
   cd examples/multiproject/pytest
   pytest tests/test_multi_project.py --qase-mode=testops_multi
   ```

### Behave

1. **Install packages in development mode**:
   ```bash
   cd qase-python
   pip install -e qase-python-commons
   pip install -e qase-behave
   ```

2. Update the API token in `qase.config.json`

3. Run the tests:
   ```bash
   cd examples/multiproject/behave
   behave tests/features/multi_project.feature --define qase-mode=testops_multi
   ```

### Tavern

1. **Install packages in development mode**:
   ```bash
   cd qase-python
   pip install -e qase-python-commons
   pip install -e qase-tavern
   ```

2. Update the API token in `qase.config.json`

3. Run the tests:
   ```bash
   cd examples/multiproject/tavern
   pytest test_multi_project.tavern.yaml --qase-mode=testops_multi
   ```

### Robot Framework

1. **Install packages in development mode**:
   ```bash
   cd qase-python
   pip install -e qase-python-commons
   pip install -e qase-robotframework
   ```

2. Update the API token in `qase.config.json`

3. Run the tests:
   ```bash
   cd examples/multiproject/robot
   robot --listener qase.robotframework.Listener tests/multi_project.robot
   ```

## Test Examples

### Single Project with Single ID

**Pytest:**
```python
@qase.project_id("DEVX", 1)
def test_example():
    assert True
```

**Behave:**
```gherkin
@qase.project_id.DEVX:1
Scenario: Example test
```

**Tavern:**
```yaml
test_name: QaseProjectID.DEVX=1 Example test
```

**Robot Framework:**
```robotframework
[Tags]    Q-PROJECT.DEVX-1
```

### Single Project with Multiple IDs

**Pytest:**
```python
@qase.project_id("DEVX", [2, 3])
def test_example():
    assert True
```

**Behave:**
```gherkin
@qase.project_id.DEVX:2,3
Scenario: Example test
```

**Tavern:**
```yaml
test_name: QaseProjectID.DEVX=2,3 Example test
```

**Robot Framework:**
```robotframework
[Tags]    Q-PROJECT.DEVX-2,3
```

### Multiple Projects

**Pytest:**
```python
@qase.project_id("DEVX", 4)
@qase.project_id("DEMO", 10)
def test_example():
    assert True
```

**Behave:**
```gherkin
@qase.project_id.DEVX:4
@qase.project_id.DEMO:10
Scenario: Example test
```

**Tavern:**
```yaml
test_name: QaseProjectID.DEVX=4 QaseProjectID.DEMO=10 Example test
```

**Robot Framework:**
```robotframework
[Tags]    Q-PROJECT.DEVX-4    Q-PROJECT.DEMO-10
```

## What to Expect

When you run the examples:

1. **Test runs will be created** in both DEVX and DEMO projects
2. **Test results will be sent** to the appropriate projects based on the test case IDs specified
3. **Each project will have its own test run** with the configured title and description
4. **Results will appear** in both projects' dashboards

## Installation Notes

**Important:** Since multi-project support is a new feature, you need to install the packages in **development mode** (editable install) to use the local source code with new changes:

```bash
# From the root of qase-python repository
cd qase-python

# Install commons (required by all reporters)
pip install -e qase-python-commons

# Install the specific reporter you want to use
pip install -e qase-pytest      # For pytest
pip install -e qase-behave      # For behave
pip install -e qase-tavern      # For tavern
pip install -e qase-robotframework  # For robotframework
```

The `-e` flag installs packages in "editable" mode, which means changes to the source code will be immediately available without reinstalling.

## Notes

- Make sure the projects DEVX and DEMO exist in your Qase instance
- Update the API token in the configuration files before running
- Test case IDs used in examples (1, 2, 3, etc.) should exist in your projects or be created
- The `default_project` setting is used when a test doesn't specify a project mapping
- **You must install packages in development mode** to use the new multi-project features
