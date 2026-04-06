Feature: Field metadata tests

  @qase.id:201 @qase.fields:{"severity":"blocker"}
  Scenario: Test with severity blocker
    Given a passing condition

  @qase.id:202 @qase.fields:{"priority":"high"}
  Scenario: Test with priority high
    Given a passing condition

  @qase.id:203 @qase.fields:{"layer":"e2e"}
  Scenario: Test with layer e2e
    Given a passing condition

  @qase.id:204 @qase.fields:{"description":"Verifies_description_field"}
  Scenario: Test with description
    Given a passing condition

  @qase.id:205 @qase.fields:{"preconditions":"User_is_logged_in","postconditions":"Session_is_active"}
  Scenario: Test with preconditions and postconditions
    Given a passing condition

  @qase.id:206 @qase.fields:{"severity":"critical","priority":"high","layer":"api"}
  Scenario: Test with multiple fields
    Given a passing condition
