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
