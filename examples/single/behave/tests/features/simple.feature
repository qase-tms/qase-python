Feature: Basic Qase Integration
  Demonstrates basic Qase Behave Reporter features including
  test case linking, metadata fields, and test organization.

  # ============================================================================
  # @qase.id - Link scenario to existing Qase test case
  # ============================================================================

  @qase.id:1
  Scenario: User can login with valid credentials
    Given a registered user exists with email "user@example.com"
    When the user enters valid credentials
    And clicks the login button
    Then the user should be redirected to dashboard
    And should see welcome message

  @qase.id:2
  Scenario: User cannot login with invalid password
    Given a registered user exists with email "user@example.com"
    When the user enters wrong password
    And clicks the login button
    Then an error message should be displayed
    And the user should remain on login page

  @qase.id:3,4,5
  Scenario: User session management
    Given the user is logged in
    When the user clicks logout
    Then the session should be terminated
    And the user should be redirected to login page

  # ============================================================================
  # @qase.fields - Add metadata to test case
  # ============================================================================

  @qase.fields:{"severity":"critical","priority":"high","layer":"e2e"}
  Scenario: Payment processing completes successfully
    Given a user has items in shopping cart
    And valid payment method is configured
    When the user initiates checkout
    And confirms the payment
    Then the order should be created
    And confirmation email should be sent

  @qase.fields:{"description":"Verifies password reset flow works correctly","preconditions":"User must have registered email"}
  Scenario: Password reset email is sent
    Given user exists with email "forgot@example.com"
    When user requests password reset
    Then reset email should be sent
    And email should contain reset link

  # ============================================================================
  # Combined annotations
  # ============================================================================

  @qase.id:10 @qase.fields:{"severity":"blocker","description":"Critical checkout validation"}
  Scenario: Cart total is calculated correctly
    Given the following items in cart:
      | name     | price  | quantity |
      | Laptop   | 999.99 | 1        |
      | Mouse    | 29.99  | 2        |
      | Keyboard | 79.99  | 1        |
    When the cart total is calculated
    Then the total should be 1139.96

  # ============================================================================
  # Tests without Qase ID (auto-created in Qase)
  # ============================================================================

  Scenario: Search returns relevant results
    Given products exist in the catalog
    When user searches for "laptop"
    Then search results should contain "laptop"
    And results should be sorted by relevance

  Scenario: User profile can be updated
    Given the user is logged in
    And viewing profile page
    When user updates their name to "John Doe"
    And saves the changes
    Then profile should be updated successfully
