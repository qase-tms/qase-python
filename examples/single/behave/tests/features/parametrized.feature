Feature: Parametrized Tests

  Scenario Outline: Test with parameters success
    Given I have a test with parameters "<param1>" and "<param2>"
    When I run it
    Then it should pass

    Examples:
      | param1 | param2 |
      | 1      | 2      |
      | 3      | 4      |
      | 5      | 6      |


  Scenario Outline: Test with parameters failed
    Given I have a test with parameters "<param1>" and "<param2>"
    When I run it
    Then it should fail

    Examples:
      | param1 | param2 |
      | 1      | 2      |
      | 3      | 4      |
      | 5      | 6      |
