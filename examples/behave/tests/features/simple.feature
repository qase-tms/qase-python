Feature: Simple tests

  Scenario: Test without annotations success
    Given I have a simple test
    When I run it
    Then it should pass

  Scenario: Test without annotations failed
    Given I have a simple test
    When I run it
    Then it should fail

  @qase.id:1
  Scenario: Test with QaseID success
    Given I have a simple test
    When I run it
    Then it should pass

  @qase.id:2
  Scenario: Test with QaseID failed
    Given I have a simple test
    When I run it
    Then it should fail

  @qase.fields:{"description":"It_is_simple_test"}
  Scenario: Test with Fields success
    Given I have a simple test
    When I run it
    Then it should pass

  @qase.fields:{"description":"It_is_simple_test"}
  Scenario: Test with Fields failed
    Given I have a simple test
    When I run it
    Then it should fail
