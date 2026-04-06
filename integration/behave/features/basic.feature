Feature: Basic pass/fail/skip tests

  @qase.id:101
  Scenario: Simple passing test
    Given a passing condition

  @qase.id:102
  Scenario: Simple failing test
    Given a failing condition

  @qase.id:103
  Scenario: Skipped test
    Given a skipped condition
