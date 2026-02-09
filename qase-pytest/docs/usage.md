# Qase Integration in Pytest

This guide provides comprehensive instructions for integrating Qase with Pytest.

> **Configuration:** For complete configuration reference including all available options, environment variables, and examples, see the [qase-python-commons README](../../qase-python-commons/README.md).

---

## Table of Contents

- [Adding QaseID](#adding-qaseid)
- [Adding Title](#adding-title)
- [Adding Fields](#adding-fields)
- [Adding Suite](#adding-suite)
- [Ignoring Tests](#ignoring-tests)
- [Muting Tests](#muting-tests)
- [Working with Attachments](#working-with-attachments)
- [Working with Steps](#working-with-steps)
- [Working with Parameters](#working-with-parameters)
- [Multi-Project Support](#multi-project-support)
- [Running Tests](#running-tests)
- [Complete Examples](#complete-examples)

---

## Adding QaseID

Link your automated tests to existing test cases in Qase by specifying the test case ID.

### Single ID

```python
from qase.pytest import qase

@qase.id(1)
def test_single_case():
    assert True
```

### Multiple IDs

Link one test to multiple test cases:

```python
from qase.pytest import qase

@qase.id([2, 3, 4])
def test_linked_to_multiple_cases():
    assert True
```

### Multi-Project Support

To send test results to multiple Qase projects simultaneously, see the [Multi-Project Support Guide](MULTI_PROJECT.md).

---

## Adding Title

Set a custom title for the test case (overrides the auto-generated title from the function name):

```python
from qase.pytest import qase

@qase.title("Verify user can log in with valid credentials")
def test_login():
    assert True
```

---

## Adding Fields

Add metadata to your test cases using fields. Both system and custom fields are supported.

### System Fields

| Field | Description | Example Values |
|-------|-------------|----------------|
| `description` | Test case description | Any text |
| `preconditions` | Test preconditions | Any text (supports Markdown) |
| `postconditions` | Test postconditions | Any text |
| `severity` | Test severity | `blocker`, `critical`, `major`, `normal`, `minor`, `trivial` |
| `priority` | Test priority | `high`, `medium`, `low` |
| `layer` | Test layer | `e2e`, `api`, `unit` |

### Example

```python
from qase.pytest import qase

@qase.fields(
    ("severity", "critical"),
    ("priority", "high"),
    ("layer", "e2e"),
    ("description", "Verify user can complete checkout process"),
    ("preconditions", "- User is logged in\n- Cart has items"),
)
def test_checkout():
    assert True
```

### Custom Fields

Custom fields defined in your Qase project can also be set:

```python
from qase.pytest import qase

@qase.fields(
    ("browser", "chrome"),
    ("environment", "staging"),
    ("custom_field_slug", "custom_value"),
)
def test_with_custom_fields():
    assert True
```

---

## Adding Suite

Organize tests into suites and sub-suites.

### Simple Suite

```python
from qase.pytest import qase

@qase.suite("Authentication")
def test_login():
    assert True
```

### Suite with Description

```python
from qase.pytest import qase

@qase.suite("Authentication", "Tests for user authentication flows")
def test_login():
    assert True
```

### Nested Suites

Use dot notation to create nested suite hierarchy:

```python
from qase.pytest import qase

@qase.suite("Authentication.Login")
def test_valid_login():
    assert True

@qase.suite("Authentication.Login.OAuth")
def test_google_login():
    assert True

@qase.suite("Authentication.Logout")
def test_logout():
    assert True
```

This creates the following structure in Qase:
```
Authentication/
├── Login/
│   ├── test_valid_login
│   └── OAuth/
│       └── test_google_login
└── Logout/
    └── test_logout
```

---

## Ignoring Tests

Exclude a test from Qase reporting. The test still executes in pytest, but results are not sent to Qase:

```python
from qase.pytest import qase

@qase.ignore()
def test_not_reported_to_qase():
    # This test runs but is not reported
    assert True
```

---

## Muting Tests

Mark a test as muted. Muted tests are reported to Qase but do not affect the test run status:

```python
from qase.pytest import qase

@qase.muted()
def test_flaky_test():
    # Results are reported but won't fail the run
    assert True
```

---

## Working with Attachments

Attach files, screenshots, logs, and other content to your test results.

### Attach File from Path

```python
from qase.pytest import qase

def test_with_file():
    qase.attach("/path/to/screenshot.png")
    qase.attach("/path/to/logs.txt")
    assert True
```

### Attach with MIME Type

```python
from qase.pytest import qase

def test_with_mime_type():
    qase.attach(
        ("/path/to/data.json", "application/json"),
        ("/path/to/report.xml", "application/xml"),
    )
    assert True
```

### Attach Content from Memory

```python
from qase.pytest import qase

def test_with_content():
    # Text content
    qase.attach(("Log content here", "text/plain", "test.log"))

    # Binary content (e.g., screenshot)
    screenshot_bytes = driver.get_screenshot_as_png()
    qase.attach((screenshot_bytes, "image/png", "screenshot.png"))

    assert True
```

### Attach in Fixtures

```python
import pytest
from qase.pytest import qase

@pytest.fixture
def browser():
    driver = create_driver()
    yield driver

    # Attach screenshot on teardown
    screenshot = driver.get_screenshot_as_png()
    qase.attach((screenshot, "image/png", "final_state.png"))

    driver.quit()
```

> For more details, see [Attachments Guide](ATTACHMENTS.md).

---

## Working with Steps

Define test steps for detailed reporting in Qase.

### Using Decorator

```python
from qase.pytest import qase

@qase.step("Open login page")
def open_login_page():
    # Implementation
    pass

@qase.step("Enter username '{username}'")
def enter_username(username):
    # Implementation
    pass

@qase.step("Click login button")
def click_login():
    # Implementation
    pass

def test_login_flow():
    open_login_page()
    enter_username("testuser")
    click_login()
    assert True
```

### Using Context Manager

```python
from qase.pytest import qase

def test_checkout():
    with qase.step("Add item to cart"):
        # Add item logic
        pass

    with qase.step("Proceed to checkout"):
        # Checkout logic
        pass

    with qase.step("Complete payment"):
        # Payment logic
        pass

    assert True
```

### Nested Steps

```python
from qase.pytest import qase

def test_complex_flow():
    with qase.step("Setup test data"):
        with qase.step("Create user"):
            pass
        with qase.step("Create product"):
            pass

    with qase.step("Execute test"):
        pass

    assert True
```

### Steps with Expected Results

```python
from qase.pytest import qase

@qase.step("Verify user is redirected", expected="User sees dashboard page")
def verify_redirect():
    # Verification logic
    pass
```

> For more details, see [Steps Guide](STEPS.md).

---

## Working with Parameters

Report parameterized test data to Qase.

### Basic Parameterized Test

```python
import pytest
from qase.pytest import qase

@pytest.mark.parametrize("username,password", [
    ("user1", "pass1"),
    ("user2", "pass2"),
])
@qase.id(1)
def test_login(username, password):
    assert login(username, password)
```

### Ignoring Specific Parameters

Exclude specific parameters from Qase reports using `@qase.ignore_parameters()`:

```python
import pytest
from qase.pytest import qase

@pytest.mark.parametrize("browser", ["chrome", "firefox"])
@pytest.mark.parametrize("user", ["user1", "user2"])
@qase.ignore_parameters("browser")  # Only 'user' will be reported
def test_login(browser, user):
    assert True
```

### Using parametrize_ignore

Replace `@pytest.mark.parametrize` entirely to ignore those parameters:

```python
from qase.pytest import qase

@qase.parametrize_ignore(
    "internal_data",
    [("data1",), ("data2",)],
    ids=["case1", "case2"]
)
@pytest.mark.parametrize("visible_param", ["a", "b"])
def test_with_mixed_params(internal_data, visible_param):
    # internal_data is not reported, visible_param is reported
    assert True
```

### Combining Both Approaches

```python
import pytest
from qase.pytest import qase

@qase.parametrize_ignore("debug_data", ["d1", "d2"])
@pytest.mark.parametrize("browser", ["chrome", "firefox"])
@pytest.mark.parametrize("user", ["alice", "bob"])
@qase.ignore_parameters("browser")
def test_complex_params(debug_data, browser, user):
    # Only 'user' is reported to Qase
    # 'debug_data' ignored via parametrize_ignore
    # 'browser' ignored via ignore_parameters
    assert True
```

> For more details, see [Parameters Guide](PARAMETERS.md).

---

## Multi-Project Support

Send test results to multiple Qase projects simultaneously using `@qase.project_id()`:

```python
from qase.pytest import qase

@qase.project_id("PROJ1", 1, 2)  # IDs 1, 2 in PROJ1
@qase.project_id("PROJ2", 10)    # ID 10 in PROJ2
def test_shared_functionality():
    assert True
```

For detailed configuration, examples, and troubleshooting, see the [Multi-Project Support Guide](MULTI_PROJECT.md).

---

## Running Tests

### Basic Execution

```sh
pytest
```

### With CLI Options

```sh
pytest \
    --qase-mode=testops \
    --qase-testops-project=PROJ \
    --qase-testops-api-token=your_token \
    --qase-testops-run-title="Regression Run"
```

### With Environment Variables

```sh
export QASE_MODE=testops
export QASE_TESTOPS_PROJECT=PROJ
export QASE_TESTOPS_API_TOKEN=your_token
pytest
```

### With Existing Test Run

Report results to an existing test run (useful for parallel execution or mixed manual/automated runs):

```sh
pytest --qase-testops-run-id=123
```

### With Test Plan

Run only tests from a specific test plan:

```sh
pytest --qase-testops-plan-id=456
```

### With Environment

```sh
pytest --qase-environment=staging
```

### With Log Capture

```sh
pytest --qase-pytest-capture-logs=true
```

---

## Complete Examples

### Full Test Example

```python
import pytest
from qase.pytest import qase

@qase.id(1)
@qase.title("User Registration Flow")
@qase.suite("Authentication.Registration")
@qase.fields(
    ("severity", "critical"),
    ("priority", "high"),
    ("layer", "e2e"),
    ("description", "Verify new user can register successfully"),
    ("preconditions", "- Application is running\n- Email service is available"),
)
def test_user_registration(browser):
    with qase.step("Open registration page"):
        browser.goto("/register")

    with qase.step("Fill registration form"):
        browser.fill("#email", "test@example.com")
        browser.fill("#password", "SecurePass123")

    with qase.step("Submit form"):
        browser.click("#submit")

    with qase.step("Verify success message"):
        assert browser.text_content(".success") == "Registration successful"


@qase.id([2, 3])
@qase.title("User Login Test")
@qase.suite("Authentication.Login")
@pytest.mark.parametrize("email,password,expected", [
    ("valid@example.com", "correct", True),
    ("valid@example.com", "wrong", False),
])
def test_login(browser, email, password, expected):
    with qase.step(f"Login with {email}"):
        result = login(browser, email, password)

    assert result == expected


@qase.ignore()
def test_work_in_progress():
    # Not reported to Qase
    pass
```

### Example Project Structure

```
my-project/
├── qase.config.json
├── conftest.py
├── tests/
│   ├── test_auth.py
│   ├── test_checkout.py
│   └── test_api.py
└── requirements.txt
```

---

## Troubleshooting

### Tests Not Appearing in Qase

1. Verify `mode` is set to `testops` (not `off` or `report`)
2. Check API token has write permissions
3. Verify project code is correct
4. Check for errors in console output (enable `debug: true`)

### Attachments Not Uploading

1. Verify file path exists and is readable
2. Check file size (large files may take time)
3. Enable debug logging to see upload status

### Results Going to Wrong Test Cases

1. Verify QaseID matches the test case ID in Qase
2. Check for duplicate IDs in your test suite
3. Verify you're using the correct project code

### Parameterized Tests Creating Duplicates

Use `@qase.ignore_parameters()` to exclude parameters that shouldn't differentiate test cases.

---

## See Also

- [Configuration Reference](../../qase-python-commons/README.md)
- [Attachments Guide](ATTACHMENTS.md)
- [Steps Guide](STEPS.md)
- [Parameters Guide](PARAMETERS.md)
- [Multi-Project Support](MULTI_PROJECT.md)
- [Upgrade Guide](UPGRADE.md)
