Feature: Tags tests

  @qase.id:901 @qase.tags:smoke
  Scenario: Test with single tag
    Given a passing condition

  @qase.id:902 @qase.tags:smoke,regression,api
  Scenario: Test with multiple tags
    Given a passing condition
