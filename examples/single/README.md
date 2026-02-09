# Single Project Examples

Examples for reporting test results to a single Qase project using `mode: testops`.

## Frameworks

| Framework | Directory | Run Command |
|-----------|-----------|-------------|
| Pytest | [pytest/](./pytest/) | `pytest tests/` |
| Behave | [behave/](./behave/) | `behave --format=qase.behave.formatter:QaseFormatter` |
| Robot Framework | [robot/](./robot/) | `robot --listener qase.robotframework.Listener tests/` |
| Tavern | [tavern/](./tavern/) | `pytest` |

## Quick Start

1. Navigate to the framework directory:
   ```bash
   cd examples/single/pytest
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure credentials (choose one method):

   **Option A: Edit config file**
   ```bash
   # Edit qase.config.json and replace <token> and <project_code>
   ```

   **Option B: Use environment variables**
   ```bash
   export QASE_TESTOPS_API_TOKEN=your_token
   export QASE_TESTOPS_PROJECT=your_project_code
   ```

4. Run tests (see framework-specific commands above)

## Test Case Linking

Use `@qase.id()` to link tests to existing test cases in Qase:

**Pytest:**
```python
@qase.id(1)
def test_example():
    pass

@qase.id([1, 2, 3])  # Multiple IDs
def test_multiple():
    pass
```

**Behave:**
```gherkin
@qase.id:1
Scenario: Example test
```

**Robot Framework:**
```robotframework
Test Case Name
    [Tags]    Q-1
```

**Tavern:**
```yaml
test_name: QaseID=1 Example test
```

## What's in Each Example

### Pytest

| File | Demonstrates |
|------|--------------|
| `test_basic.py` | `@qase.id`, `@qase.title`, `@qase.fields`, `@qase.description`, `@qase.priority`, `@qase.severity` |
| `test_attachments.py` | `qase.attach()` with files and byte data |
| `test_steps.py` | `@qase.step` decorator and `with qase.step()` context |
| `test_*_profiler.py` | Database profiling examples (SQLite, PostgreSQL, MySQL, MongoDB, Redis) |

### Behave

| File | Demonstrates |
|------|--------------|
| `simple.feature` | Basic test with `@qase.id` and `@qase.fields` |
| `attachments.feature` | File attachments in BDD tests |
| `suites.feature` | Test suite organization with `@qase.suite` |
| `parametrized.feature` | Scenario outlines with examples |

### Robot Framework

| File | Demonstrates |
|------|--------------|
| `simple.robot` | Basic tests with `Q-ID` tags |
| `parametrized.robot` | Data-driven tests with parameters |

### Tavern

| File | Demonstrates |
|------|--------------|
| `test_simple.tavern.yaml` | Basic API test without Qase ID |
| `test_with_id.tavern.yaml` | API test with `QaseID=N` in test name |

## Configuration

Each framework directory contains a `qase.config.json` with recommended settings.

Example configuration:
```json
{
  "mode": "testops",
  "fallback": "report",
  "testops": {
    "api": {
      "token": "<token>",
      "host": "qase.io"
    },
    "project": "<project_code>",
    "run": {
      "title": "Example run",
      "complete": true
    }
  }
}
```

For complete configuration options, see [qase-python-commons](../../qase-python-commons/README.md).
