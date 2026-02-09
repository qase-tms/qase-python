*** Settings ***
Documentation    Basic examples demonstrating Qase Robot Framework Reporter features.
...              Shows test case linking, metadata fields, and step tracking.
Library          Collections
Library          String

*** Variables ***
${BASE_URL}      https://api.example.com
${VALID_EMAIL}   user@example.com
${VALID_PASS}    SecurePass123

*** Test Cases ***

# ==============================================================================
# Q-ID tag - Link test to existing Qase test case
# ==============================================================================

User Can Login With Valid Credentials
    [Documentation]    Verifies successful login flow with valid credentials
    [Tags]    Q-1
    Open Login Page
    Enter Email    ${VALID_EMAIL}
    Enter Password    ${VALID_PASS}
    Click Login Button
    Verify Dashboard Is Displayed

User Cannot Login With Invalid Password
    [Documentation]    Verifies error handling for invalid password
    [Tags]    Q-2
    Open Login Page
    Enter Email    ${VALID_EMAIL}
    Enter Password    wrong_password
    Click Login Button
    Verify Error Message Is Displayed    Invalid credentials

Test Linked To Multiple Cases
    [Documentation]    Test linked to multiple Qase test cases
    [Tags]    Q-3    Q-4    Q-5
    Open Login Page
    Verify Login Page Elements

# ==============================================================================
# qase.fields tag - Add metadata to test case
# ==============================================================================

Payment Processing Test
    [Documentation]    Critical test for payment processing
    [Tags]    Q-10    qase.fields:{"severity":"blocker","priority":"high"}
    Initialize Payment
    Enter Payment Details    4242424242424242    12/25    123
    Submit Payment
    Verify Payment Status    approved

Cart Total Calculation
    [Tags]    qase.fields:{"severity":"critical","layer":"unit","description":"Verifies shopping cart calculations"}
    Create Empty Cart
    Add Item To Cart    Laptop    999.99    1
    Add Item To Cart    Mouse     29.99     2
    Add Item To Cart    Keyboard  79.99     1
    Verify Cart Total    1139.96

# ==============================================================================
# qase.ignore tag - Exclude test from Qase reporting
# ==============================================================================

Debug Test For Local Development
    [Documentation]    This test is excluded from Qase reporting
    [Tags]    qase.ignore
    Log    This test runs locally but won't be reported to Qase
    Should Be True    ${TRUE}

# ==============================================================================
# Automatic step tracking - Each keyword is reported as a step
# ==============================================================================

E2E User Registration Flow
    [Documentation]    Complete user registration flow with step tracking
    [Tags]    Q-20    qase.fields:{"layer":"e2e"}
    # Each keyword below is automatically reported as a step in Qase
    Open Registration Page
    Fill Registration Form    newuser@example.com    SecureP@ss1    John Doe
    Accept Terms And Conditions
    Submit Registration
    Verify Confirmation Email Sent
    Activate Account
    Verify Account Is Active

API Response Validation
    [Documentation]    API test with multiple validation steps
    [Tags]    Q-21    qase.fields:{"layer":"api"}
    Send GET Request    /api/users
    Verify Status Code    200
    Verify Response Contains    users
    Verify Response Is JSON

# ==============================================================================
# Combined test with all features
# ==============================================================================

Complete Checkout Flow
    [Documentation]    Full checkout flow demonstrating all reporter features
    [Tags]    Q-30    qase.fields:{"severity":"critical","priority":"high","layer":"e2e","description":"Complete e-commerce checkout flow"}
    # Setup
    Create User Session
    Create Empty Cart
    # Add products
    Add Item To Cart    Wireless Mouse    29.99    2
    Add Item To Cart    USB-C Hub         49.99    1
    # Apply discount
    Apply Coupon Code    SAVE10
    Verify Discount Applied    10
    # Shipping
    Enter Shipping Address    John Doe    123 Main St    San Francisco    94105
    Select Shipping Method    express
    # Payment
    Enter Payment Details    4242424242424242    12/25    123
    Submit Payment
    # Verification
    Verify Order Created
    Verify Confirmation Email Sent

*** Keywords ***

# ==============================================================================
# Authentication Keywords
# ==============================================================================

Open Login Page
    Log    Opening login page
    ${page}=    Set Variable    login
    Should Not Be Empty    ${page}

Enter Email
    [Arguments]    ${email}
    Log    Entering email: ${email}
    Should Match Regexp    ${email}    .*@.*\\..*

Enter Password
    [Arguments]    ${password}
    Log    Entering password (hidden)
    Should Not Be Empty    ${password}

Click Login Button
    Log    Clicking login button

Verify Dashboard Is Displayed
    Log    Verifying dashboard is displayed
    Should Be True    ${TRUE}

Verify Error Message Is Displayed
    [Arguments]    ${message}
    Log    Verifying error message: ${message}
    Should Not Be Empty    ${message}

Verify Login Page Elements
    Log    Verifying login page elements exist

# ==============================================================================
# Payment Keywords
# ==============================================================================

Initialize Payment
    Log    Initializing payment system

Enter Payment Details
    [Arguments]    ${card_number}    ${expiry}    ${cvv}
    Log    Entering payment details
    ${card_length}=    Get Length    ${card_number}
    Should Be Equal As Numbers    ${card_length}    16

Submit Payment
    Log    Submitting payment

Verify Payment Status
    [Arguments]    ${expected_status}
    Log    Verifying payment status: ${expected_status}
    Should Be Equal    ${expected_status}    approved

# ==============================================================================
# Cart Keywords
# ==============================================================================

Create Empty Cart
    ${cart}=    Create Dictionary    items=@{EMPTY}    total=0
    Set Test Variable    ${CART}    ${cart}
    Log    Created empty cart

Add Item To Cart
    [Arguments]    ${name}    ${price}    ${quantity}
    Log    Adding to cart: ${name} x ${quantity} @ $${price}
    ${item}=    Create Dictionary    name=${name}    price=${price}    quantity=${quantity}
    ${items}=    Get From Dictionary    ${CART}    items
    Append To List    ${items}    ${item}
    ${total}=    Get From Dictionary    ${CART}    total
    ${item_total}=    Evaluate    ${price} * ${quantity}
    ${new_total}=    Evaluate    ${total} + ${item_total}
    Set To Dictionary    ${CART}    total=${new_total}

Verify Cart Total
    [Arguments]    ${expected}
    ${actual}=    Get From Dictionary    ${CART}    total
    ${diff}=    Evaluate    abs(${actual} - ${expected})
    Should Be True    ${diff} < 0.01

Apply Coupon Code
    [Arguments]    ${code}
    Log    Applying coupon: ${code}
    Set Test Variable    ${COUPON}    ${code}

Verify Discount Applied
    [Arguments]    ${percent}
    Log    Verifying ${percent}% discount applied
    Should Be True    ${percent} > 0

# ==============================================================================
# Registration Keywords
# ==============================================================================

Open Registration Page
    Log    Opening registration page

Fill Registration Form
    [Arguments]    ${email}    ${password}    ${name}
    Log    Filling registration form for ${name}
    Should Match Regexp    ${email}    .*@.*\\..*
    ${pass_length}=    Get Length    ${password}
    Should Be True    ${pass_length} >= 8

Accept Terms And Conditions
    Log    Accepting terms and conditions

Submit Registration
    Log    Submitting registration

Verify Confirmation Email Sent
    Log    Verification email sent

Activate Account
    Log    Activating account

Verify Account Is Active
    Log    Account is active

# ==============================================================================
# API Keywords
# ==============================================================================

Send GET Request
    [Arguments]    ${endpoint}
    Log    Sending GET request to ${endpoint}
    ${response}=    Create Dictionary    status=200    body={"users":[]}
    Set Test Variable    ${RESPONSE}    ${response}

Verify Status Code
    [Arguments]    ${expected}
    ${actual}=    Get From Dictionary    ${RESPONSE}    status
    Should Be Equal As Numbers    ${actual}    ${expected}

Verify Response Contains
    [Arguments]    ${field}
    ${body}=    Get From Dictionary    ${RESPONSE}    body
    Should Contain    ${body}    ${field}

Verify Response Is JSON
    Log    Response is valid JSON

# ==============================================================================
# Shipping Keywords
# ==============================================================================

Enter Shipping Address
    [Arguments]    ${name}    ${street}    ${city}    ${zip}
    Log    Entering shipping address for ${name}
    ${address}=    Create Dictionary    name=${name}    street=${street}    city=${city}    zip=${zip}
    Set Test Variable    ${SHIPPING}    ${address}

Select Shipping Method
    [Arguments]    ${method}
    Log    Selecting shipping method: ${method}
    Set Test Variable    ${SHIPPING_METHOD}    ${method}

# ==============================================================================
# Order Keywords
# ==============================================================================

Create User Session
    Log    Creating user session
    ${session}=    Create Dictionary    user_id=1    token=abc123
    Set Test Variable    ${SESSION}    ${session}

Verify Order Created
    Log    Order created successfully
    ${order}=    Create Dictionary    id=ORD-001    status=confirmed
    Set Test Variable    ${ORDER}    ${order}
