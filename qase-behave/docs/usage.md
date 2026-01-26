# Qase Integration in Behave

This guide demonstrates how to integrate Qase with Behave, providing instructions on how to add Qase IDs,
fields and suites to your test cases.

---

## Adding QaseID to a Test

To associate a QaseID with a test in Behave, use the `@qase.id` tag. This tag accepts a single integer
representing the test's ID in Qase.

### Example:

```gherkin
Feature: Example tests

  @qase.id:1
  Scenario: Example test
    Given I have a simple test
    When I run it
    Then it should pass
```

### Multi-Project Support

To send test results to multiple projects with different test case IDs, use the `@qase.project_id.PROJECT_CODE:IDS` tag:

```gherkin
Feature: Example tests

  # Single project with multiple IDs
  @qase.project_id.PROJ1:123,124
  Scenario: Example test with multiple IDs
    Given I have a simple test
    When I run it
    Then it should pass

  # Multiple projects with different IDs
  @qase.project_id.PROJ1:123
  @qase.project_id.PROJ2:456
  Scenario: Example test for multiple projects
    Given I have a simple test
    When I run it
    Then it should pass

  # Multiple projects with multiple IDs each
  @qase.project_id.PROJ1:123,124
  @qase.project_id.PROJ2:456,457
  Scenario: Complex multi-project test
    Given I have a simple test
    When I run it
    Then it should pass
```

**Note:** When using `@qase.project_id`, the test results will be sent to all specified projects. Make sure to configure `testops_multi` mode in your `qase.config.json` file.

---

## Adding Fields to a Test

The `qase.fields` tag allows you to add additional metadata to a test case. You can specify multiple fields to
enhance test case information in Qase. In field values, underscores (_) should be used instead of spaces. The reporter
will automatically replace all underscores with spaces.

### System Fields:

- `description` — Description of the test case.
- `preconditions` — Preconditions for the test case.
- `postconditions` — Postconditions for the test case.
- `severity` — Severity of the test case (e.g., `critical`, `major`).
- `priority` — Priority of the test case (e.g., `high`, `low`).
- `layer` — Test layer (e.g., `UI`, `API`).

### Example:

```gherkin
Feature: Example tests

  @qase.fields:{"description":"It_is_simple_test"}
  Scenario: Example test
    Given I have a simple test
    When I run it
    Then it should pass
```

---

## Adding a Suite to a Test

To assign a suite or sub-suite to a test, use the `qase.suite` tag. It can receive a suite name, and optionally a
sub-suite, both as strings.

### Example:

```gherkin
Feature: Example tests

  @qase.suite:MySuite
  Scenario: Example test
    Given I have a simple test
    When I run it
    Then it should pass

  @qase.suite:MySuite||SubSuite
  Scenario: Example test
    Given I have a simple test
    When I run it
    Then it should pass
```

---

## Ignoring a Test in Qase

To exclude a test from being reported to Qase (while still executing the test in Behave), use the `qase.ignore`
tag. The test will run, but its result will not be sent to Qase.

### Example:

```gherkin
Feature: Example tests

  @qase.ignore
  Scenario: Example test
    Given I have a simple test
    When I run it
    Then it should pass
```

---

## Adding Attachments to Tests

Qase Behave supports attaching files and content to test results. You can attach files or content either to the test case (scenario level) or to a specific test step.

### Attach to Test Case

Use `qase.attach()` to attach files or content to the test case. This is useful for screenshots, logs, or data files that are relevant to the entire test scenario.

### Example:

```gherkin
Feature: Example tests

  @qase.id:1
  Scenario: Example test with attachments
    Given I have a test with a file
    When I attach a screenshot
    Then the attachment should be in the test case
```

```python
from behave import *
from qase.behave import qase

@given('I have a test with a file')
def step_impl(context):
    # Attach an existing file to the test case
    qase.attach(file_path="/path/to/your/file.txt")

@when('I attach a screenshot')
def step_impl(context):
    # Attach binary data (e.g., screenshot) to the test case
    screenshot_data = b"binary_screenshot_data"
    qase.attach(
        content=screenshot_data,
        file_name="screenshot.png",
        mime_type="image/png"
    )
```

### Attach to Test Step

Use `qase.attach_to_step()` to attach files or content directly to a specific test step. This is useful when you want to associate attachments with a particular step execution.

### Example:

```gherkin
Feature: Example tests

  @qase.id:1
  Scenario: Example test with step attachments
    Given I have a test
    When I attach a screenshot to this step
    Then the attachment should be in the step
```

```python
from behave import *
from qase.behave import qase

@when('I attach a screenshot to this step')
def step_impl(context):
    # Attach binary data to the current step
    screenshot_data = b"binary_screenshot_data"
    qase.attach_to_step(
        content=screenshot_data,
        file_name="step_screenshot.png",
        mime_type="image/png"
    )
    
    # Attach text content to the current step
    qase.attach_to_step(
        content="Step execution log",
        file_name="step_log.txt"
    )
```

### Method Parameters

Both `qase.attach()` and `qase.attach_to_step()` accept the same parameters:

- `file_path`: Path to the file to attach (mutually exclusive with `content`)
- `content`: Content to attach as string or bytes (mutually exclusive with `file_path`)
- `file_name`: Name for the attachment (auto-detected from `file_path` if not provided)
- `mime_type`: MIME type of the attachment (auto-detected if not provided)

**Notes:**

- Either `file_path` or `content` must be provided, but not both
- If `file_name` is not provided, it will be derived from `file_path` or default to "attachment.txt"
- If `mime_type` is not provided, it will be auto-detected from the file extension or default to "text/plain"
- Attachments are automatically included in the test result when the scenario completes
