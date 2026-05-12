Feature: Adding numbers

  @qase.id=11 @qase.suite=Math.Outline
  Scenario Outline: Adding two numbers
    Given I have <a> and <b>
    Then their sum is <c>

    Examples:
      | a | b | c  |
      | 1 | 2 | 3  |
      | 5 | 7 | 12 |
      | 0 | 0 | 0  |
