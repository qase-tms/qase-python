Feature: Multi-Project Tests
  Tests demonstrating multi-project support in Behave

  @qase.project_id.DEVX:1
  Scenario: Single project with single ID
    Given I have a simple test
    When I run it
    Then it should pass

  @qase.project_id.DEVX:2,3
  Scenario: Single project with multiple IDs
    Given I have a test with multiple IDs
    When I execute it
    Then it should succeed

  @qase.project_id.DEVX:4
  @qase.project_id.DEMO:10
  Scenario: Multiple projects with single ID each
    Given I have a test for multiple projects
    When I run it
    Then it should be reported to both projects

  @qase.project_id.DEVX:5,6
  @qase.project_id.DEMO:11,12
  Scenario: Multiple projects with multiple IDs each
    Given I have a complex multi-project test
    When I execute it
    Then it should work correctly

  @qase.project_id.DEVX:7
  Scenario: Failed test for DEVX project
    Given I have a test that will fail
    When I run it
    Then it should fail intentionally

  @qase.project_id.DEMO:13
  Scenario: Passed test for DEMO project
    Given I have a test that will pass
    When I run it
    Then it should succeed

  Scenario: Test without any ID
    Given I have a test without ID
    When I run it
    Then it should be sent to first project
