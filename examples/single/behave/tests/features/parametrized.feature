Feature: Parametrized Scenarios
  Demonstrates Scenario Outlines with Examples tables.
  Each row in Examples table creates a separate test result in Qase.

  # ============================================================================
  # Basic parametrization - Login with different user roles
  # ============================================================================

  @qase.id:40
  Scenario Outline: User login with different roles
    Given user with role "<role>" exists
    When user logs in with email "<email>"
    Then user should have access to "<accessible_pages>"

    Examples: Standard users
      | role    | email              | accessible_pages          |
      | viewer  | viewer@example.com | dashboard,profile         |
      | editor  | editor@example.com | dashboard,profile,content |

    Examples: Admin users
      | role        | email                | accessible_pages                      |
      | admin       | admin@example.com    | dashboard,profile,content,settings    |
      | super_admin | super@example.com    | dashboard,profile,content,settings,users |

  # ============================================================================
  # Validation scenarios - Input validation testing
  # ============================================================================

  @qase.id:41 @qase.fields:{"severity":"normal","layer":"unit"}
  Scenario Outline: Email validation
    When email "<email>" is validated
    Then validation result should be "<result>"
    And error message should be "<error_message>"

    Examples: Valid emails
      | email               | result | error_message |
      | user@example.com    | valid  | none          |
      | test.user@mail.org  | valid  | none          |
      | admin+tag@site.net  | valid  | none          |

    Examples: Invalid emails
      | email           | result  | error_message         |
      | invalid         | invalid | Missing @ symbol      |
      | @nodomain.com   | invalid | Missing local part    |
      | user@           | invalid | Missing domain        |
      | user@.com       | invalid | Invalid domain format |

  # ============================================================================
  # API testing - HTTP status codes
  # ============================================================================

  @qase.id:42 @qase.fields:{"layer":"api"}
  Scenario Outline: API endpoint returns correct status
    Given API endpoint "<endpoint>" exists
    When "<method>" request is sent
    Then response status should be <status_code>
    And response should contain "<expected_field>"

    Examples: GET endpoints
      | endpoint     | method | status_code | expected_field |
      | /api/users   | GET    | 200         | users          |
      | /api/posts   | GET    | 200         | posts          |
      | /api/invalid | GET    | 404         | error          |

    Examples: POST endpoints
      | endpoint          | method | status_code | expected_field |
      | /api/users        | POST   | 201         | id             |
      | /api/unauthorized | POST   | 401         | error          |

  # ============================================================================
  # Business logic - Pricing calculations
  # ============================================================================

  @qase.id:43 @qase.fields:{"severity":"critical"}
  Scenario Outline: Discount calculation
    Given base price is <base_price>
    And discount type is "<discount_type>"
    And discount value is <discount_value>
    When discount is applied
    Then final price should be <final_price>

    Examples: Percentage discounts
      | base_price | discount_type | discount_value | final_price |
      | 100.00     | percentage    | 10             | 90.00       |
      | 250.00     | percentage    | 20             | 200.00      |
      | 500.00     | percentage    | 50             | 250.00      |

    Examples: Fixed amount discounts
      | base_price | discount_type | discount_value | final_price |
      | 100.00     | fixed         | 15             | 85.00       |
      | 250.00     | fixed         | 50             | 200.00      |
      | 500.00     | fixed         | 100            | 400.00      |

  # ============================================================================
  # Edge cases - Boundary value testing
  # ============================================================================

  @qase.id:44
  Scenario Outline: Password length validation
    When password "<password>" is checked
    Then password should be "<validity>"
    And message should be "<message>"

    Examples: Boundary values
      | password        | validity | message                            |
      | abc             | invalid  | Password must be at least 8 chars  |
      | abcdefg         | invalid  | Password must be at least 8 chars  |
      | abcdefgh        | valid    | Password meets requirements        |
      | abcdefghi       | valid    | Password meets requirements        |
      | a234567890123456789012345678901 | valid | Password meets requirements |
      | a2345678901234567890123456789012 | invalid | Password exceeds 32 chars |
