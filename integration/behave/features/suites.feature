Feature: Suite organization tests

  @qase.id:301 @qase.suite:Authentication
  Scenario: Test in Authentication suite
    Given a passing condition

  @qase.id:302 @qase.suite:Authentication||OAuth
  Scenario: Test in nested suite
    Given a passing condition

  @qase.id:303 @qase.suite:Authentication||OAuth||Google
  Scenario: Test in deeply nested suite
    Given a passing condition
