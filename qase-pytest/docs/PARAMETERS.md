# Parameters in Pytest

This guide covers how to work with parameterized tests and control which parameters are reported to Qase.

---

## Overview

When using `@pytest.mark.parametrize`, Qase Pytest Reporter automatically captures parameter values and includes them in test results. This helps distinguish between different test variations.

You can control which parameters are reported using:
- `@qase.ignore_parameters()` — Exclude specific parameters from reports
- `@qase.parametrize_ignore()` — Replace parametrize entirely with ignored parameters

---

## Basic Parameterized Tests

Parameters are automatically captured and reported:

```python
import pytest
from qase.pytest import qase

@pytest.mark.parametrize("username,password", [
    ("user1", "pass1"),
    ("user2", "pass2"),
    ("user3", "pass3"),
])
@qase.id(1)
def test_login(username, password):
    assert login(username, password)
```

Each parameter combination creates a separate test result in Qase with the parameter values visible.

---

## Ignoring Parameters

### Using `@qase.ignore_parameters()`

Exclude specific parameters from Qase reports while still using them in tests:

```python
import pytest
from qase.pytest import qase

@pytest.mark.parametrize("browser", ["chrome", "firefox", "safari"])
@pytest.mark.parametrize("user", ["admin", "regular"])
@qase.ignore_parameters("browser")  # Only 'user' is reported
def test_login(browser, user):
    # browser parameter is used but not reported to Qase
    driver = create_driver(browser)
    login(driver, user)
    assert True
```

### Multiple Parameters

Ignore multiple parameters:

```python
import pytest
from qase.pytest import qase

@pytest.mark.parametrize("env", ["staging", "production"])
@pytest.mark.parametrize("browser", ["chrome", "firefox"])
@pytest.mark.parametrize("user_type", ["admin", "user"])
@qase.ignore_parameters("env", "browser")  # Only 'user_type' is reported
def test_cross_browser(env, browser, user_type):
    assert True
```

---

## Using `@qase.parametrize_ignore()`

Replace `@pytest.mark.parametrize` entirely — parameters are used in tests but never reported:

```python
from qase.pytest import qase

@qase.parametrize_ignore(
    "internal_id,debug_data",
    [
        ("id-001", {"verbose": True}),
        ("id-002", {"verbose": False}),
    ],
    ids=["verbose", "quiet"]
)
def test_with_internal_data(internal_id, debug_data):
    # internal_id and debug_data are used but not reported
    process(internal_id, debug_data)
    assert True
```

### With Test IDs

```python
from qase.pytest import qase

@qase.parametrize_ignore(
    "test_input,expected",
    [
        ("3+5", 8),
        ("2+4", 6),
        ("6*9", 54),
    ],
    ids=["addition_1", "addition_2", "multiplication"]
)
def test_eval(test_input, expected):
    assert eval(test_input) == expected
```

---

## Combining Approaches

Use both decorators together for fine-grained control:

```python
import pytest
from qase.pytest import qase

@qase.parametrize_ignore("debug_info", [{"log": True}, {"log": False}])
@pytest.mark.parametrize("browser", ["chrome", "firefox"])
@pytest.mark.parametrize("user", ["alice", "bob"])
@pytest.mark.parametrize("env", ["staging", "prod"])
@qase.ignore_parameters("browser", "env")
@qase.id(1)
def test_complex(debug_info, browser, user, env):
    # Only 'user' is reported to Qase
    # debug_info - ignored via parametrize_ignore
    # browser, env - ignored via ignore_parameters
    assert True
```

---

## Common Use Cases

### Browser/Environment Testing

When running the same test across multiple browsers or environments:

```python
import pytest
from qase.pytest import qase

@pytest.mark.parametrize("browser", ["chrome", "firefox", "safari"])
@qase.ignore_parameters("browser")
@qase.id(1)
def test_login_flow(browser):
    # Same test case in Qase, different browser runs
    driver = get_driver(browser)
    assert login(driver, "user", "pass")
```

### Test Data vs Test Logic

Separate test data (that should be tracked) from test configuration (that shouldn't):

```python
import pytest
from qase.pytest import qase

@pytest.mark.parametrize("username,expected_role", [
    ("admin@example.com", "admin"),
    ("user@example.com", "user"),
])
@pytest.mark.parametrize("timeout", [5, 10, 30])  # Infrastructure config
@qase.ignore_parameters("timeout")
def test_user_role(username, expected_role, timeout):
    # username and expected_role are reported (test data)
    # timeout is not reported (test configuration)
    user = fetch_user(username, timeout=timeout)
    assert user.role == expected_role
```

### Sensitive Data

Exclude sensitive information from reports:

```python
import pytest
from qase.pytest import qase

@pytest.mark.parametrize("user", ["admin", "regular"])
@pytest.mark.parametrize("api_key", [API_KEY_1, API_KEY_2])
@qase.ignore_parameters("api_key")
def test_api_access(user, api_key):
    # api_key is used but not visible in Qase reports
    response = make_api_call(user, api_key)
    assert response.status_code == 200
```

### Debug/Verbose Modes

Exclude debug-only parameters:

```python
import pytest
from qase.pytest import qase

@qase.parametrize_ignore(
    "debug_mode,verbose",
    [(True, True), (False, False)],
    ids=["debug", "normal"]
)
@pytest.mark.parametrize("feature", ["login", "checkout", "search"])
def test_features(debug_mode, verbose, feature):
    # feature is reported
    # debug_mode and verbose are not
    run_test(feature, debug=debug_mode, verbose=verbose)
    assert True
```

---

## Global Parameter Exclusion

Use configuration to exclude parameters across all tests:

### Via Config File

```json
{
  "excludeParams": ["password", "api_key", "token", "secret"]
}
```

### Via Environment Variable

```bash
export QASE_EXCLUDE_PARAMS="password,api_key,token,secret"
```

This applies to all tests without needing decorators.

---

## How Parameters Appear in Qase

When parameters are reported, they appear in the test result:

```
Test: test_login[admin-staging]
Parameters:
  - user: admin
  - environment: staging
```

Ignored parameters are completely omitted from the report.

---

## Best Practices

### Report Meaningful Parameters

Report parameters that:
- Distinguish test variations
- Are relevant to understanding failures
- Help identify which scenarios are covered

### Ignore Infrastructure Parameters

Ignore parameters that:
- Don't affect test logic (browser, timeout)
- Contain sensitive data
- Are for debugging only
- Create noise in reports

### Use Descriptive IDs

```python
@pytest.mark.parametrize("status,expected", [
    (200, "success"),
    (404, "not_found"),
    (500, "error"),
], ids=["success_response", "not_found_response", "server_error"])
def test_handle_response(status, expected):
    assert handle(status) == expected
```

---

## Troubleshooting

### All Parameter Combinations Creating Separate Test Cases

If you want one test case with multiple runs:
1. Use `@qase.ignore_parameters()` for varying parameters
2. Or use global `excludeParams` configuration

### Parameters Not Appearing

1. Check if parameters are in `excludeParams` config
2. Verify `@qase.ignore_parameters()` isn't applied
3. Enable debug logging to see parameter processing

### Wrong Parameters Ignored

Decorator order matters:
```python
# Parameters are processed in decorator order
@pytest.mark.parametrize("a", [1, 2])
@pytest.mark.parametrize("b", [3, 4])
@qase.ignore_parameters("a")  # Must come after parametrize
def test_order(a, b):
    pass
```

---

## See Also

- [Usage Guide](usage.md)
- [Multi-Project Support](MULTI_PROJECT.md)
- [Configuration Reference](../../qase-python-commons/README.md)
