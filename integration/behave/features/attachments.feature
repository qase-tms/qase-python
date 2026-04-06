Feature: Attachment tests

  @qase.id:601
  Scenario: Test with file attachment
    Given I attach a sample file

  @qase.id:602
  Scenario: Test with content attachment
    Given I attach content as json

  @qase.id:701,702
  Scenario: Test linked to multiple Qase test cases
    Given a passing condition
