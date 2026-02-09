# Behave Examples

Examples demonstrating Qase Behave Reporter features.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure credentials in `qase.config.json`:
   - Replace `<token>` with your [API token](https://app.qase.io/user/api/token)
   - Replace `<project_code>` with your project code

   Or use environment variables:
   ```bash
   export QASE_TESTOPS_API_TOKEN=your_token
   export QASE_TESTOPS_PROJECT=your_project_code
   ```

## Run Tests

```bash
# Run all tests
behave --format=qase.behave.formatter:QaseFormatter

# Run specific feature
behave --format=qase.behave.formatter:QaseFormatter tests/features/simple.feature

# Run with console output
behave --format=qase.behave.formatter:QaseFormatter --format=pretty
```

## Examples

| File | Description |
|------|-------------|
| `simple.feature` | Basic tests with `@qase.id` and `@qase.fields` tags |
| `attachments.feature` | File attachments in BDD scenarios |
| `suites.feature` | Test suite organization with `@qase.suite` |
| `parametrized.feature` | Scenario Outlines with Examples tables |

## Code Examples

### Link to Test Case

```gherkin
@qase.id:1
Scenario: Test linked to case 1
  Given some precondition
  When action is performed
  Then expected result occurs
```

### Add Metadata

```gherkin
@qase.id:1 @qase.fields:{"severity":"critical","priority":"high"}
Scenario: Test with metadata
  Given some precondition
  When action is performed
  Then expected result occurs
```

### Test Suites

```gherkin
@qase.suite:Authentication
Feature: Login functionality

  @qase.id:1
  Scenario: Valid login
    Given user is on login page
    When user enters valid credentials
    Then user is logged in
```

### Parametrized Tests

```gherkin
@qase.id:10
Scenario Outline: Login with different users
  Given user "<username>" exists
  When user logs in with password "<password>"
  Then login result is "<result>"

  Examples:
    | username | password | result  |
    | admin    | admin123 | success |
    | user     | wrong    | failure |
```

### Ignore Test

```gherkin
@qase.ignore
Scenario: This test will not be reported to Qase
  Given some condition
  When action happens
  Then result is ignored
```

### Attachments

```gherkin
Scenario: Test with attachment
  Given I have a file to attach
  When I attach the file "screenshot.png"
  Then the attachment is added to the test result
```

Step implementation:
```python
from behave import when
from qase.behave import qase

@when('I attach the file "{filename}"')
def attach_file(context, filename):
    qase.attach(f"/path/to/{filename}")
```

## Documentation

- [Behave Reporter README](../../../qase-behave/README.md)
- [Usage Guide](../../../qase-behave/docs/usage.md)
- [Configuration Reference](../../../qase-python-commons/README.md)
