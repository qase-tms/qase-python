@qase.suite:Authentication
Feature: User Authentication
  Demonstrates test suite organization using @qase.suite tag.
  All scenarios in this feature are organized under "Authentication" suite.

  # ============================================================================
  # Single-level suite organization
  # ============================================================================

  @qase.id:100
  Scenario: Login with email and password
    Given the login page is displayed
    When user enters email "user@example.com"
    And user enters password "SecurePass123"
    And clicks submit button
    Then user should be authenticated
    And redirected to dashboard

  @qase.id:101
  Scenario: Login with remember me option
    Given the login page is displayed
    When user enters valid credentials
    And checks "remember me" checkbox
    And clicks submit button
    Then user should be authenticated
    And session should persist for 30 days

  # ============================================================================
  # Nested suite organization
  # ============================================================================

  @qase.id:102 @qase.suite:Authentication||OAuth
  Scenario: Login with Google OAuth
    Given the login page is displayed
    When user clicks "Sign in with Google"
    And completes Google authentication
    Then user should be authenticated
    And profile should be synced from Google

  @qase.id:103 @qase.suite:Authentication||OAuth
  Scenario: Login with GitHub OAuth
    Given the login page is displayed
    When user clicks "Sign in with GitHub"
    And completes GitHub authentication
    Then user should be authenticated
    And profile should be synced from GitHub

  @qase.id:104 @qase.suite:Authentication||OAuth||Error_Handling
  Scenario: OAuth provider returns error
    Given the login page is displayed
    When user clicks "Sign in with Google"
    And Google returns authentication error
    Then error message should be displayed
    And user should remain on login page

  # ============================================================================
  # Security suite
  # ============================================================================

  @qase.id:105 @qase.suite:Authentication||Security
  Scenario: Account lockout after failed attempts
    Given user has account with email "user@example.com"
    When user enters wrong password 5 times
    Then account should be locked
    And lockout notification email should be sent

  @qase.id:106 @qase.suite:Authentication||Security
  Scenario: Two-factor authentication
    Given user has 2FA enabled
    And user enters valid credentials
    When 2FA code is requested
    And user enters valid 2FA code
    Then user should be authenticated

  @qase.id:107 @qase.suite:Authentication||Security||Session
  Scenario: Session timeout after inactivity
    Given user is logged in
    And user is inactive for 30 minutes
    When user performs an action
    Then session should be expired
    And user should be redirected to login
