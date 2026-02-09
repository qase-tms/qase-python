Feature: Test Attachments
  As a test developer
  I want to attach files and content to my test results
  So that I can provide additional context for test failures

  @qase.id:300
  Scenario: Attach file to test
    Given I have a test with attachments
    When I attach a file to the test
    Then the attachments should be included in the test result

  @qase.id:301
  Scenario: Attach text content
    Given I have a test with attachments
    When I attach content as text
    Then the attachments should be included in the test result

  @qase.id:302
  Scenario: Attach JSON data
    Given I have a test with attachments
    When I attach JSON data
    Then the attachments should be included in the test result

  @qase.id:303
  Scenario: Attach screenshot
    Given I want to attach a screenshot
    When I attach the screenshot
    Then the attachments should be included in the test result

  @qase.id:304
  Scenario: Add comments to test
    Given I have a test with attachments
    When I add a comment about the test
    Then the attachments should be included in the test result

  @qase.id:305
  Scenario: Add debug information
    Given I have a test with attachments
    When I add debug information
    Then the attachments should be included in the test result
