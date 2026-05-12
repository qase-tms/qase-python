Feature: Login

  @qase.id=1 @qase.suite=Login.Smoke @qase.severity=critical
  Scenario: Successful login
    Given the user is on the login page
    When the user enters valid credentials
    Then the user should see the dashboard
