Feature: Parametrized tests

  @qase.id:501
  Scenario Outline: Parametrized addition test
    Given the first number is <a>
    And the second number is <b>
    Then the sum is <result>

    Examples:
      | a | b | result |
      | 1 | 2 | 3      |
      | 4 | 5 | 9      |
