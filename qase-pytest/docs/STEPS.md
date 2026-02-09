# Test Steps in Pytest

This guide covers how to define and report test steps for detailed execution tracking in Qase.

---

## Overview

Test steps provide granular visibility into test execution. Each step is reported separately, showing:

- Step name and description
- Step status (passed/failed)
- Step duration
- Attachments (if any)
- Error details (on failure)

---

## Defining Steps

### Using Decorator

Annotate functions as test steps:

```python
from qase.pytest import qase

@qase.step("Open login page")
def open_login_page(browser):
    browser.goto("/login")

@qase.step("Enter credentials")
def enter_credentials(browser, username, password):
    browser.fill("#username", username)
    browser.fill("#password", password)

@qase.step("Click login button")
def click_login(browser):
    browser.click("#login-btn")

def test_login_flow(browser):
    open_login_page(browser)
    enter_credentials(browser, "user", "pass")
    click_login(browser)
    assert browser.url == "/dashboard"
```

### Using Context Manager

Use the context manager for inline steps:

```python
from qase.pytest import qase

def test_checkout_flow(browser):
    with qase.step("Add item to cart"):
        browser.click("#add-to-cart")
        assert browser.locator(".cart-count").text_content() == "1"

    with qase.step("Proceed to checkout"):
        browser.click("#checkout")
        assert "/checkout" in browser.url

    with qase.step("Complete payment"):
        browser.fill("#card", "4111111111111111")
        browser.click("#pay")
        assert browser.locator(".success").is_visible()
```

### Dynamic Step Names

Include parameters in step names for better traceability:

```python
from qase.pytest import qase

@qase.step("Login as '{username}'")
def login_as(browser, username, password):
    browser.fill("#username", username)
    browser.fill("#password", password)
    browser.click("#login")

def test_user_roles(browser):
    login_as(browser, "admin", "admin123")  # Step: "Login as 'admin'"
    assert is_admin_dashboard_visible(browser)
```

---

## Nested Steps

Create hierarchical step structures:

```python
from qase.pytest import qase

@qase.step("Create test user")
def create_user():
    pass

@qase.step("Create test product")
def create_product():
    pass

def test_order_creation(browser):
    with qase.step("Setup test data"):
        create_user()
        create_product()

    with qase.step("Create order"):
        with qase.step("Add product to cart"):
            browser.click("#add-to-cart")

        with qase.step("Checkout"):
            browser.click("#checkout")
            browser.click("#confirm")

    with qase.step("Verify order created"):
        assert browser.locator(".order-id").is_visible()
```

This creates the following step hierarchy:
```
├── Setup test data
│   ├── Create test user
│   └── Create test product
├── Create order
│   ├── Add product to cart
│   └── Checkout
└── Verify order created
```

---

## Steps with Expected Results

Define expected results for documentation and verification:

```python
from qase.pytest import qase

@qase.step("Submit form", expected="Form is submitted and success message appears")
def submit_form(browser):
    browser.click("#submit")
    assert browser.locator(".success").is_visible()

@qase.step("Verify redirect", expected="User is redirected to dashboard page")
def verify_redirect(browser):
    assert browser.url.endswith("/dashboard")
```

---

## Steps with Attachments

Attach content to a specific step:

```python
from qase.pytest import qase

def test_with_step_attachments(browser):
    with qase.step("Fill form"):
        browser.fill("#name", "Test User")
        browser.fill("#email", "test@example.com")

    with qase.step("Submit and verify"):
        browser.click("#submit")

        # Attach screenshot to this step
        screenshot = browser.screenshot()
        qase.attach((screenshot, "image/png", "after_submit.png"))

        assert browser.locator(".success").is_visible()
```

---

## Step Status

Steps automatically inherit status from execution:

| Execution | Step Status |
|-----------|-------------|
| Completes normally | Passed |
| Raises AssertionError | Failed |
| Raises other exception | Invalid |

### Step Failure Behavior

When a step fails:
1. The step is marked as failed
2. The error message is captured
3. Subsequent steps in the same test may still execute (depending on test structure)
4. The overall test is marked as failed

```python
from qase.pytest import qase

def test_with_failing_step():
    with qase.step("First step"):
        assert True  # Passes

    with qase.step("Failing step"):
        assert False  # Fails - step marked as failed

    with qase.step("Third step"):
        # This step still executes but test already failed
        assert True
```

---

## Best Practices

### Keep Steps Atomic

Each step should represent a single action or verification:

```python
# Good: One action per step
@qase.step("Click login button")
def click_login(browser):
    browser.click("#login-btn")

@qase.step("Enter username")
def enter_username(browser, username):
    browser.fill("#username", username)

# Avoid: Multiple actions in one step
@qase.step("Fill form and submit")  # Too broad
def fill_and_submit(browser):
    browser.fill("#username", "user")
    browser.fill("#password", "pass")
    browser.click("#submit")
```

### Use Descriptive Names

```python
# Good: Clear action description
@qase.step("Verify user is redirected to dashboard after login")
def verify_dashboard_redirect(browser):
    assert "/dashboard" in browser.url

# Avoid: Vague names
@qase.step("Check page")  # What page? What check?
def check(browser):
    pass
```

### Include Context in Step Names

```python
# Good: Include relevant context
@qase.step("Add product '{product_name}' to cart")
def add_to_cart(browser, product_name):
    browser.click(f"[data-product='{product_name}'] .add-to-cart")

# Better than generic:
@qase.step("Add product")  # Which product?
def add_to_cart(browser, product_name):
    pass
```

### Group Related Steps

```python
from qase.pytest import qase

def test_e2e_purchase(browser):
    # Authentication group
    with qase.step("User authentication"):
        with qase.step("Navigate to login"):
            browser.goto("/login")
        with qase.step("Enter credentials"):
            login(browser, "user", "pass")

    # Purchase group
    with qase.step("Complete purchase"):
        with qase.step("Select product"):
            select_product(browser, "Widget")
        with qase.step("Checkout"):
            checkout(browser)

    # Verification group
    with qase.step("Verify purchase"):
        assert order_confirmation_visible(browser)
```

---

## Common Patterns

### Page Object Steps

```python
from qase.pytest import qase

class LoginPage:
    def __init__(self, browser):
        self.browser = browser

    @qase.step("Open login page")
    def open(self):
        self.browser.goto("/login")

    @qase.step("Enter username '{username}'")
    def enter_username(self, username):
        self.browser.fill("#username", username)

    @qase.step("Enter password")
    def enter_password(self, password):
        self.browser.fill("#password", password)

    @qase.step("Click login button")
    def click_login(self):
        self.browser.click("#login")

def test_login(browser):
    login_page = LoginPage(browser)
    login_page.open()
    login_page.enter_username("testuser")
    login_page.enter_password("password123")
    login_page.click_login()
    assert browser.url == "/dashboard"
```

### API Testing Steps

```python
import requests
from qase.pytest import qase

@qase.step("Create user via API")
def create_user(name, email):
    response = requests.post("/api/users", json={"name": name, "email": email})
    assert response.status_code == 201
    return response.json()["id"]

@qase.step("Get user by ID")
def get_user(user_id):
    response = requests.get(f"/api/users/{user_id}")
    assert response.status_code == 200
    return response.json()

@qase.step("Delete user")
def delete_user(user_id):
    response = requests.delete(f"/api/users/{user_id}")
    assert response.status_code == 204

def test_user_crud():
    user_id = create_user("Test", "test@example.com")
    user = get_user(user_id)
    assert user["name"] == "Test"
    delete_user(user_id)
```

### Setup/Teardown Steps

```python
import pytest
from qase.pytest import qase

@pytest.fixture
def test_user():
    with qase.step("Setup: Create test user"):
        user = create_test_user()

    yield user

    with qase.step("Teardown: Delete test user"):
        delete_user(user.id)

def test_user_profile(test_user):
    with qase.step("View user profile"):
        profile = get_profile(test_user.id)
        assert profile is not None
```

---

## Troubleshooting

### Steps Not Appearing

1. Verify the step decorator/context is properly imported from `qase.pytest`
2. Check that steps are executed within a test context
3. Enable debug logging to trace step recording

### Nested Steps Flattened

Ensure you're using the context manager correctly for nesting:

```python
# Correct: Nested context managers
with qase.step("Parent step"):
    with qase.step("Child step"):
        pass

# Incorrect: Sequential, not nested
with qase.step("Step 1"):
    pass
with qase.step("Step 2"):  # Not nested under Step 1
    pass
```

### Step Duration Shows 0

Steps need measurable execution time. Very fast steps may show 0ms duration. This is normal for simple operations.

### Steps Not Reporting Failure Details

Ensure the exception is raised within the step context:

```python
# Correct: Exception within step
with qase.step("Verify result"):
    assert result == expected  # Failure captured in step

# Incorrect: Exception outside step
with qase.step("Get result"):
    result = get_result()
assert result == expected  # Failure not associated with step
```

---

## See Also

- [Usage Guide](usage.md)
- [Attachments Guide](ATTACHMENTS.md)
- [Configuration Reference](../../qase-python-commons/README.md)
