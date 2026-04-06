Feature: Step tracking tests

  @qase.id:401
  Scenario: Test with multiple steps
    Given a user opens the app
    When the user performs an action
    Then the result is verified

  @qase.id:402
  Scenario: Test with failing step
    Given a user opens the app
    When the user triggers a failure
    Then the result is verified
