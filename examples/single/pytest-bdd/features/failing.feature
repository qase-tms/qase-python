Feature: Math

  @qase.id=10 @qase.suite=Math.Failure @qase.severity=major
  Scenario: A failing assertion in the middle step
    Given a calculator
    When I add 2 and 2
    Then the result should be 5
