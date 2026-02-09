*** Settings ***
Documentation    Examples demonstrating data-driven testing with Qase Robot Framework Reporter.
...              Shows test templates and parameter tracking in Qase.
Library          Collections

*** Variables ***
# User credentials for different roles
@{VIEWER_ACCESS}     dashboard    profile
@{EDITOR_ACCESS}     dashboard    profile    content
@{ADMIN_ACCESS}      dashboard    profile    content    settings    users

*** Test Cases ***

# ==============================================================================
# Data-driven testing with Test Template
# ==============================================================================

Login With Different User Roles
    [Documentation]    Verify different user roles have appropriate access
    [Tags]    Q-40
    [Template]    Verify User Role Access
    viewer      viewer@example.com      @{VIEWER_ACCESS}
    editor      editor@example.com      @{EDITOR_ACCESS}
    admin       admin@example.com       @{ADMIN_ACCESS}

Email Validation Test Cases
    [Documentation]    Test email validation with various inputs
    [Tags]    Q-41    qase.fields:{"layer":"unit"}
    [Template]    Validate Email Format
    # Valid emails
    user@example.com        valid       Email is valid
    test.user@mail.org      valid       Email is valid
    admin+tag@site.net      valid       Email is valid
    # Invalid emails
    invalid                 invalid     Missing @ symbol
    @nodomain.com           invalid     Missing local part
    user@                   invalid     Missing domain

HTTP Status Code Validation
    [Documentation]    Verify API endpoints return correct status codes
    [Tags]    Q-42    qase.fields:{"layer":"api"}
    [Template]    Verify API Response
    /api/users       GET     200
    /api/posts       GET     200
    /api/invalid     GET     404
    /api/users       POST    201
    /api/protected   GET     401

Discount Calculation Tests
    [Documentation]    Verify discount calculations for different types
    [Tags]    Q-43    qase.fields:{"severity":"critical"}
    [Template]    Calculate And Verify Discount
    # Percentage discounts
    100.00    percentage    10      90.00
    250.00    percentage    20      200.00
    500.00    percentage    50      250.00
    # Fixed amount discounts
    100.00    fixed         15      85.00
    250.00    fixed         50      200.00
    500.00    fixed         100     400.00

Password Strength Validation
    [Documentation]    Test password validation with boundary values
    [Tags]    Q-44
    [Template]    Validate Password Strength
    # Too short
    abc             invalid     Password must be at least 8 characters
    abcdefg         invalid     Password must be at least 8 characters
    # Valid length
    abcdefgh        valid       Password meets requirements
    Secure@Pass1    valid       Password meets requirements
    # Edge cases
    12345678        weak        Password needs mixed characters
    ABCDEFGH        weak        Password needs mixed characters

Currency Conversion Tests
    [Documentation]    Test currency conversion calculations
    [Tags]    Q-45    qase.fields:{"layer":"unit"}
    [Template]    Convert And Verify Currency
    100.00    USD    EUR    0.85    85.00
    100.00    USD    GBP    0.73    73.00
    100.00    EUR    USD    1.18    118.00
    50.00     GBP    EUR    1.16    58.00

# ==============================================================================
# Test with variables tracking
# ==============================================================================

Shopping Cart Total With Tax
    [Documentation]    Calculate cart total with tax for different states
    [Tags]    Q-46    qase.params:[state, tax_rate]
    [Template]    Calculate Cart Total With Tax
    CA    0.0725    107.25
    NY    0.08      108.00
    TX    0.0625    106.25
    OR    0.00      100.00

*** Keywords ***

Verify User Role Access
    [Arguments]    ${role}    ${email}    @{expected_pages}
    Log    Testing user role: ${role} (${email})
    ${user}=    Create Dictionary    role=${role}    email=${email}
    Set Test Variable    ${USER}    ${user}
    FOR    ${page}    IN    @{expected_pages}
        Log    Verifying access to: ${page}
        Should Not Be Empty    ${page}
    END
    ${page_count}=    Get Length    ${expected_pages}
    Log    User has access to ${page_count} pages

Validate Email Format
    [Arguments]    ${email}    ${expected_result}    ${expected_message}
    Log    Validating email: ${email}
    ${is_valid}=    Run Keyword And Return Status
    ...    Should Match Regexp    ${email}    ^[^@]+@[^@]+\\.[^@]+$
    ${result}=    Set Variable If    ${is_valid}    valid    invalid
    ${message}=    Set Variable If    ${is_valid}    Email is valid
    ...    ELSE IF    '@' not in '${email}'    Missing @ symbol
    ...    ELSE IF    '${email}'.startswith('@')    Missing local part
    ...    ELSE    Missing domain
    Should Be Equal    ${result}    ${expected_result}

Verify API Response
    [Arguments]    ${endpoint}    ${method}    ${expected_status}
    Log    ${method} request to ${endpoint}
    # Simulate API response based on endpoint
    ${status}=    Set Variable If
    ...    '${endpoint}' == '/api/invalid'    404
    ...    '${endpoint}' == '/api/protected'    401
    ...    '${method}' == 'POST'    201
    ...    200
    Should Be Equal As Numbers    ${status}    ${expected_status}

Calculate And Verify Discount
    [Arguments]    ${base_price}    ${discount_type}    ${discount_value}    ${expected_final}
    Log    Base price: $${base_price}, Discount: ${discount_value} (${discount_type})
    ${final_price}=    Run Keyword If    '${discount_type}' == 'percentage'
    ...    Evaluate    ${base_price} - (${base_price} * ${discount_value} / 100)
    ...    ELSE
    ...    Evaluate    ${base_price} - ${discount_value}
    ${diff}=    Evaluate    abs(${final_price} - ${expected_final})
    Should Be True    ${diff} < 0.01    Expected $${expected_final}, got $${final_price}

Validate Password Strength
    [Arguments]    ${password}    ${expected_validity}    ${expected_message}
    Log    Checking password strength
    ${length}=    Get Length    ${password}
    ${has_upper}=    Run Keyword And Return Status
    ...    Should Match Regexp    ${password}    [A-Z]
    ${has_lower}=    Run Keyword And Return Status
    ...    Should Match Regexp    ${password}    [a-z]
    ${has_digit}=    Run Keyword And Return Status
    ...    Should Match Regexp    ${password}    [0-9]
    ${has_special}=    Run Keyword And Return Status
    ...    Should Match Regexp    ${password}    [!@#$%^&*]
    # Determine validity
    ${validity}=    Set Variable If
    ...    ${length} < 8    invalid
    ...    not (${has_upper} and ${has_lower} and ${has_digit})    weak
    ...    valid
    Should Be Equal    ${validity}    ${expected_validity}

Convert And Verify Currency
    [Arguments]    ${amount}    ${from_currency}    ${to_currency}    ${rate}    ${expected}
    Log    Converting ${amount} ${from_currency} to ${to_currency} at rate ${rate}
    ${result}=    Evaluate    ${amount} * ${rate}
    ${diff}=    Evaluate    abs(${result} - ${expected})
    Should Be True    ${diff} < 0.01

Calculate Cart Total With Tax
    [Arguments]    ${state}    ${tax_rate}    ${expected_total}
    Log    Calculating cart total for ${state} with tax rate ${tax_rate}
    ${subtotal}=    Set Variable    100.00
    ${tax}=    Evaluate    ${subtotal} * ${tax_rate}
    ${total}=    Evaluate    ${subtotal} + ${tax}
    ${diff}=    Evaluate    abs(${total} - ${expected_total})
    Should Be True    ${diff} < 0.01
