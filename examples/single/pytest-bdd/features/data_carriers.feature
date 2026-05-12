Feature: Data carriers

  @qase.id=12 @qase.suite=API.Payloads
  Scenario: Step with a data table and a docstring
    Given the following users:
      | name  | role  |
      | Alice | admin |
      | Bob   | user  |
    When I send the payload:
      """
      {"username": "alice", "active": true}
      """
    Then the request succeeds
