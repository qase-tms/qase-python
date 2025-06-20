# Qase Integration in Pytest

This guide demonstrates how to integrate Qase with Pytest, providing instructions on how to add Qase IDs, fields, suites, and other metadata to your test cases.

---

## Adding QaseID to a Test

To associate a QaseID with a test in Pytest, use the `@qase.id` decorator.

```python
from qase.pytest import qase

@qase.id(1)
def test_example():
    assert True

@qase.id([2, 3])  # Multiple IDs
def test_multiple_ids():
    assert True
```

---

## Adding Title to a Test

To set a custom title for a test case:

```python
from qase.pytest import qase

@qase.title("User Login Test")
def test_login():
    assert True
```

---

## Adding Fields to a Test

The `qase.fields` decorator allows you to add additional metadata to a test case.

```python
from qase.pytest import qase

@qase.fields(
    ("priority", "high"),
    ("severity", "critical"),
    ("layer", "UI"),
    ("custom_field", "custom_value")
)
def test_example():
    assert True
```

---

## Adding a Suite to a Test

To assign a suite or sub-suite to a test:

```python
from qase.pytest import qase

@qase.suite("Authentication")
def test_login():
    assert True

@qase.suite("Authentication", "Login")  # With description
def test_login_with_description():
    assert True
```

### Nested Suites

You can create nested suites using dot notation:

```python
from qase.pytest import qase

@qase.suite("Authentication.Login")
def test_login():
    assert True

@qase.suite("Authentication.Logout")
def test_logout():
    assert True
```

---

## Ignoring a Test in Qase

To exclude a test from being reported to Qase (while still executing the test):

```python
from qase.pytest import qase

@qase.ignore()
def test_example():
    assert True
```

---

## Muting a Test

To mark a test as muted (it will not affect the test run status):

### Using Decorator

```python
from qase.pytest import qase

@qase.muted()
def test_example():
    assert True
```

---

## Working with Parameters

### Ignoring Parameters

To exclude specific parameters from Qase reports. Only `param1` and `param2` will be reported.

```python
from qase.pytest import qase

@qase.parametrize_ignore(
    "test_input,expected",
    [("3+5", 8), ("2+4", 6), ("6*9", 42)],
    ids=["add_3_5", "add_2_4", "multiply_6_9"]
)
@pytest.mark.parametrize(
    "param1,param2", 
    [(1, 2), (3, 4), (5, 6)], 
    ids=["param1_1_2", "param1_3_4", "param1_5_6"])
def test_eval(test_input, expected, param1, param2):
    print(param1, param2)
    assert eval(test_input) == expected
```

---

## Advanced Configuration

### Profilers

Enable profilers to collect additional data:

#### Sleep Profiler

Sleep profiler is a special profiler that allows you to measure the time taken by the test. Each sleep will be reported as a separate step with the duration of the sleep.

```bash
pytest --qase-profilers=sleep
```

```python
from qase.pytest import qase

def test_example():
    time.sleep(1)
    assert True
```

#### Network Profiler

Network profiler is a special profiler that allows you to measure the time taken by the network requests. Each network request will be reported as a separate step with the request details.

```bash
pytest --qase-profilers=network
```

```python
import requests

def test_example():
    requests.get("https://api.qase.io/v1/projects")
    assert True
```

---

### Log Capture

Capture pytest logs. All logs will be reported as a attachment to the test case.

```bash
pytest --qase-pytest-capture-logs=true
```

### XFail Status

Configure xfail status mapping:

```bash
pytest --qase-pytest-xfail-status-xfail=skipped
```

---

## Execution Plans

You can use execution plans to run only specific tests:

```bash
pytest --qase-execution-plan-path=plan.json
```

The execution plan file should contain a list of Qase IDs:

```json
[1, 2, 3, 4, 5]
```

---

## Multiple Decorators

You can combine multiple decorators:

```python
from qase.pytest import qase

@qase.id(1)
@qase.title("User Login Test")
@qase.suite("Authentication")
@qase.fields(
    ("priority", "high"),
    ("severity", "critical"),
    ("layer", "UI")
)
def test_login():
    assert True
```

---

## Examples

### Complete Test Example

```python
import pytest
from qase.pytest import qase

@qase.id(1)
@qase.title("User Registration Test")
@qase.suite("Authentication.Registration")
@qase.fields(
    ("priority", "high"),
    ("severity", "critical"),
    ("layer", "UI")
)
def test_user_registration():
    # Test implementation
    assert True

@qase.id([2, 3])
@qase.title("User Login Test")
@qase.suite("Authentication.Login")
@qase.ignore()  # This test will be ignored in Qase
def test_user_login():
    # Test implementation
    assert True

@qase.parametrize_ignore(
    "email,password",
    [("user1@example.com", "pass1"), ("user2@example.com", "pass2")],
    ids=["user1", "user2"]
)
def test_login_with_different_users(email, password):
    # Test implementation
    assert True
```

### Running Tests

```bash
# Basic run
pytest --qase-mode=testops --qase-testops-project=MYPROJECT --qase-testops-api-token=YOUR_TOKEN

# With environment and plan
pytest --qase-mode=testops --qase-testops-project=MYPROJECT --qase-testops-api-token=YOUR_TOKEN --qase-environment=staging --qase-testops-plan-id=123

# With execution plan
pytest --qase-mode=testops --qase-testops-project=MYPROJECT --qase-testops-api-token=YOUR_TOKEN --qase-execution-plan-path=plan.json

# With profilers and logs
pytest --qase-mode=testops --qase-testops-project=MYPROJECT --qase-testops-api-token=YOUR_TOKEN --qase-profilers=network,db --qase-pytest-capture-logs=true
```
