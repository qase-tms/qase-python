# Qase Integration in Behave

This guide provides comprehensive instructions for integrating Qase with Behave BDD framework.

> **Configuration:** For complete configuration reference including all available options, environment variables, and examples, see the [qase-python-commons README](../../qase-python-commons/README.md).

---

## Table of Contents

- [Adding QaseID](#adding-qaseid)
- [Adding Fields](#adding-fields)
- [Adding Suite](#adding-suite)
- [Ignoring Tests](#ignoring-tests)
- [Working with Attachments](#working-with-attachments)
- [Multi-Project Support](#multi-project-support)
- [Running Tests](#running-tests)
- [Complete Examples](#complete-examples)

---

## Adding QaseID

Link your scenarios to existing test cases in Qase using the `@qase.id` tag.

### Single ID

```gherkin
Feature: Authentication

  @qase.id:1
  Scenario: User can log in
    Given I am on the login page
    When I enter valid credentials
    Then I should see the dashboard
```

### Multiple Scenarios

```gherkin
Feature: Shopping Cart

  @qase.id:1
  Scenario: Add item to cart
    Given I am on a product page
    When I click add to cart
    Then the item should be in my cart

  @qase.id:2
  Scenario: Remove item from cart
    Given I have an item in my cart
    When I click remove
    Then my cart should be empty
```

### Multi-Project Support

To send test results to multiple Qase projects simultaneously, see the [Multi-Project Support Guide](MULTI_PROJECT.md).

---

## Adding Fields

Add metadata to your scenarios using the `@qase.fields` tag with JSON format.

### System Fields

| Field | Description | Example Values |
|-------|-------------|----------------|
| `description` | Test case description | Any text |
| `preconditions` | Test preconditions | Any text |
| `postconditions` | Test postconditions | Any text |
| `severity` | Test severity | `blocker`, `critical`, `major`, `normal`, `minor`, `trivial` |
| `priority` | Test priority | `high`, `medium`, `low` |
| `layer` | Test layer | `e2e`, `api`, `unit` |

### Example

```gherkin
Feature: Checkout

  @qase.id:1
  @qase.fields:{"severity":"critical","priority":"high","layer":"e2e"}
  Scenario: Complete purchase
    Given I have items in my cart
    When I complete checkout
    Then I should see order confirmation
```

### Multiple Fields

```gherkin
Feature: User Management

  @qase.id:1
  @qase.fields:{"description":"Verify_user_registration_flow","preconditions":"User_is_not_registered","severity":"critical"}
  Scenario: User registration
    Given I am on the registration page
    When I fill in the registration form
    And I submit the form
    Then I should see a confirmation message
```

**Note:** Use underscores (`_`) instead of spaces in field values. They will be automatically converted to spaces.

---

## Adding Suite

Organize scenarios into suites using the `@qase.suite` tag.

### Simple Suite

```gherkin
Feature: Authentication

  @qase.id:1
  @qase.suite:Authentication
  Scenario: User login
    Given I am on the login page
    When I enter valid credentials
    Then I should see the dashboard
```

### Nested Suite

Use `||` to create nested suites:

```gherkin
Feature: Authentication

  @qase.id:1
  @qase.suite:Authentication||Login
  Scenario: Valid login
    Given I am on the login page
    When I enter valid credentials
    Then I should see the dashboard

  @qase.id:2
  @qase.suite:Authentication||Login||OAuth
  Scenario: Google login
    Given I am on the login page
    When I click "Login with Google"
    Then I should be redirected to Google
```

---

## Ignoring Tests

Exclude scenarios from Qase reporting while still executing them:

```gherkin
Feature: Experimental

  @qase.ignore
  Scenario: Work in progress
    Given this feature is not ready
    Then it should not be reported to Qase
```

---

## Working with Attachments

Attach files and content to test results in step definitions.

### Attach to Test Case

```python
from behave import given, when, then
from qase.behave import qase

@when('I take a screenshot')
def step_impl(context):
    # Attach file from path
    qase.attach(file_path="/path/to/screenshot.png")

@then('I save the response')
def step_impl(context):
    # Attach content directly
    qase.attach(
        content=context.response.text,
        file_name="response.json",
        mime_type="application/json"
    )
```

### Attach to Step

```python
from behave import when
from qase.behave import qase

@when('I complete the form')
def step_impl(context):
    # Fill form...

    # Attach screenshot to this specific step
    screenshot = context.browser.get_screenshot_as_png()
    qase.attach_to_step(
        content=screenshot,
        file_name="form_completed.png",
        mime_type="image/png"
    )
```

### Method Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `file_path` | `str` | No* | Path to file to attach |
| `content` | `str` or `bytes` | No* | Content to attach |
| `file_name` | `str` | No | Custom filename |
| `mime_type` | `str` | No | MIME type (auto-detected) |

\* Either `file_path` or `content` must be provided.

> For more details, see [Attachments Guide](ATTACHMENTS.md).

---

## Multi-Project Support

Send test results to multiple Qase projects using the `@qase.project_id` tag:

```gherkin
Feature: Shared Functionality

  @qase.project_id.PROJ1:1,2
  @qase.project_id.PROJ2:10
  Scenario: Test reported to multiple projects
    Given I perform an action
    Then it should be reported to PROJ1 and PROJ2
```

For detailed configuration, examples, and troubleshooting, see the [Multi-Project Support Guide](MULTI_PROJECT.md).

---

## Running Tests

### Basic Execution

```sh
behave --format=qase.behave.formatter:QaseFormatter
```

### With Environment Variables

```sh
export QASE_MODE=testops
export QASE_TESTOPS_PROJECT=PROJ
export QASE_TESTOPS_API_TOKEN=your_token
behave --format=qase.behave.formatter:QaseFormatter
```

### With Config File

Create `qase.config.json`:

```json
{
  "mode": "testops",
  "testops": {
    "project": "PROJ",
    "api": {
      "token": "your_token"
    }
  }
}
```

Then run:

```sh
behave --format=qase.behave.formatter:QaseFormatter
```

### Run Specific Feature

```sh
behave --format=qase.behave.formatter:QaseFormatter features/login.feature
```

### With Tags

```sh
behave --format=qase.behave.formatter:QaseFormatter --tags=@smoke
```

---

## Complete Examples

### Full Feature File

```gherkin
@qase.suite:Authentication
Feature: User Authentication
  As a user
  I want to authenticate
  So that I can access my account

  Background:
    Given the application is running

  @qase.id:1
  @qase.fields:{"severity":"critical","priority":"high"}
  Scenario: Successful login
    Given I am on the login page
    When I enter username "testuser"
    And I enter password "testpass"
    And I click the login button
    Then I should see the dashboard
    And I should see "Welcome, testuser"

  @qase.id:2
  @qase.fields:{"severity":"major","priority":"medium"}
  Scenario: Failed login with invalid password
    Given I am on the login page
    When I enter username "testuser"
    And I enter password "wrongpass"
    And I click the login button
    Then I should see an error message
    And I should remain on the login page

  @qase.id:3
  @qase.suite:Authentication||Logout
  Scenario: User logout
    Given I am logged in as "testuser"
    When I click the logout button
    Then I should be redirected to the login page

  @qase.ignore
  Scenario: Password reset (WIP)
    Given I am on the login page
    When I click "Forgot password"
    Then I should see the password reset form
```

### Step Definitions with Attachments

```python
from behave import given, when, then
from qase.behave import qase

@given('I am on the login page')
def step_impl(context):
    context.browser.goto("/login")

@when('I enter username "{username}"')
def step_impl(context, username):
    context.browser.fill("#username", username)

@when('I enter password "{password}"')
def step_impl(context, password):
    context.browser.fill("#password", password)

@when('I click the login button')
def step_impl(context):
    context.browser.click("#login-btn")
    # Attach screenshot after clicking
    screenshot = context.browser.screenshot()
    qase.attach_to_step(
        content=screenshot,
        file_name="after_click.png",
        mime_type="image/png"
    )

@then('I should see the dashboard')
def step_impl(context):
    assert context.browser.url.endswith("/dashboard")

@then('I should see "{text}"')
def step_impl(context, text):
    assert text in context.browser.content()
```

### Example Project Structure

```
my-project/
├── qase.config.json
├── features/
│   ├── environment.py
│   ├── login.feature
│   ├── checkout.feature
│   └── steps/
│       ├── login_steps.py
│       └── checkout_steps.py
└── requirements.txt
```

---

## Troubleshooting

### Tests Not Appearing in Qase

1. Verify `mode` is set to `testops`
2. Check API token has write permissions
3. Verify project code is correct
4. Ensure formatter is specified: `--format=qase.behave.formatter:QaseFormatter`

### Fields Not Applying

1. Verify JSON syntax is correct
2. Use underscores instead of spaces in values
3. Check for typos in field names

### Attachments Not Uploading

1. Verify file path exists
2. Check file permissions
3. Enable debug logging: `"debug": true`

---

## See Also

- [Configuration Reference](../../qase-python-commons/README.md)
- [Attachments Guide](ATTACHMENTS.md)
- [Multi-Project Support](MULTI_PROJECT.md)
