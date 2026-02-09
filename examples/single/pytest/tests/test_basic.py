"""
Basic examples demonstrating Qase Pytest Reporter decorators.

This module shows how to use various decorators to enrich test metadata
that will be reported to Qase TestOps.
"""
from qase.pytest import qase


# ============================================================================
# @qase.id - Link test to existing Qase test case
# ============================================================================

@qase.id(1)
def test_user_login_with_valid_credentials():
    """Test linked to Qase test case #1."""
    username = "admin"
    password = "secure_password"

    # Simulate authentication
    is_authenticated = len(username) > 0 and len(password) >= 8
    assert is_authenticated, "User should be authenticated with valid credentials"


@qase.id([2, 3])
def test_user_permissions_check():
    """Test linked to multiple Qase test cases #2 and #3."""
    user_role = "admin"
    required_permissions = ["read", "write", "delete"]

    # Admin has all permissions
    user_permissions = ["read", "write", "delete"] if user_role == "admin" else ["read"]

    for permission in required_permissions:
        assert permission in user_permissions, f"Missing permission: {permission}"


# ============================================================================
# @qase.title - Custom test title in Qase
# ============================================================================

@qase.title("Verify shopping cart total calculation")
def test_cart_total():
    """Demonstrate custom title that appears in Qase instead of function name."""
    items = [
        {"name": "Laptop", "price": 999.99, "quantity": 1},
        {"name": "Mouse", "price": 29.99, "quantity": 2},
        {"name": "Keyboard", "price": 79.99, "quantity": 1},
    ]

    expected_total = 999.99 + (29.99 * 2) + 79.99
    actual_total = sum(item["price"] * item["quantity"] for item in items)

    assert abs(actual_total - expected_total) < 0.01, "Cart total should be calculated correctly"


# ============================================================================
# @qase.description - Detailed test description
# ============================================================================

@qase.description("""
This test verifies the password validation rules:
- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one digit
- At least one special character
""")
def test_password_validation():
    """Test with detailed description shown in Qase."""
    def validate_password(password: str) -> bool:
        if len(password) < 8:
            return False
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)
        return has_upper and has_lower and has_digit and has_special

    valid_password = "SecureP@ss1"
    assert validate_password(valid_password), "Password should meet all requirements"


# ============================================================================
# @qase.preconditions / @qase.postconditions - Test conditions
# ============================================================================

@qase.preconditions("""
**Prerequisites:**
- User account must exist in the system
- User must have verified email address
- Account must not be locked
""")
@qase.postconditions("""
**After test completion:**
- User session token should be valid
- Last login timestamp should be updated
- Failed login counter should be reset to 0
""")
def test_successful_login_flow():
    """Test with pre/postconditions documented in Qase."""
    user = {
        "email": "user@example.com",
        "email_verified": True,
        "account_locked": False,
    }

    # Check preconditions
    assert user["email_verified"], "Email must be verified"
    assert not user["account_locked"], "Account must not be locked"

    # Simulate login
    session = {"token": "abc123", "valid": True}
    login_timestamp = "2024-01-15T10:30:00Z"
    failed_attempts = 0

    # Verify postconditions
    assert session["valid"], "Session should be valid"
    assert login_timestamp is not None, "Login timestamp should be set"
    assert failed_attempts == 0, "Failed attempts should be reset"


# ============================================================================
# @qase.severity - Test severity level
# ============================================================================

@qase.severity("blocker")
def test_payment_processing():
    """Blocker severity - payment system must work."""
    payment = {"amount": 100.00, "currency": "USD", "status": "pending"}

    # Simulate payment processing
    payment["status"] = "completed"

    assert payment["status"] == "completed", "Payment must be processed successfully"


@qase.severity("critical")
def test_user_data_encryption():
    """Critical severity - sensitive data must be encrypted."""
    sensitive_data = "user_password_123"

    # Simulate encryption (in real code, use proper encryption)
    encrypted = sensitive_data[::-1]  # Simple reversal for demo

    assert encrypted != sensitive_data, "Data must be encrypted"


@qase.severity("major")
def test_search_functionality():
    """Major severity - core feature but not critical."""
    products = ["Laptop", "Desktop", "Tablet", "Phone"]
    query = "lap"

    results = [p for p in products if query.lower() in p.lower()]

    assert len(results) > 0, "Search should return matching results"


@qase.severity("normal")
def test_pagination():
    """Normal severity - standard functionality."""
    total_items = 100
    page_size = 10
    current_page = 3

    start_index = (current_page - 1) * page_size
    end_index = start_index + page_size

    assert start_index == 20, "Pagination start index should be correct"
    assert end_index == 30, "Pagination end index should be correct"


@qase.severity("minor")
def test_ui_theme_switching():
    """Minor severity - nice to have feature."""
    current_theme = "light"

    new_theme = "dark" if current_theme == "light" else "light"

    assert new_theme == "dark", "Theme should switch correctly"


@qase.severity("trivial")
def test_tooltip_display():
    """Trivial severity - cosmetic feature."""
    element = {"has_tooltip": True, "tooltip_text": "Click to submit"}

    assert element["has_tooltip"], "Tooltip should be displayed"


# ============================================================================
# @qase.priority - Test priority level
# ============================================================================

@qase.priority("high")
def test_authentication_service():
    """High priority test that should run first."""
    service_status = "healthy"
    assert service_status == "healthy", "Auth service must be healthy"


@qase.priority("medium")
def test_notification_delivery():
    """Medium priority - important but can wait."""
    notification = {"type": "email", "sent": True}
    assert notification["sent"], "Notification should be delivered"


@qase.priority("low")
def test_analytics_tracking():
    """Low priority - can be addressed later."""
    event = {"name": "page_view", "tracked": True}
    assert event["tracked"], "Analytics event should be tracked"


# ============================================================================
# @qase.layer - Test layer categorization
# ============================================================================

@qase.layer("unit")
def test_string_formatter():
    """Unit test - testing a single function."""
    def format_currency(amount: float, currency: str = "USD") -> str:
        symbols = {"USD": "$", "EUR": "€", "GBP": "£"}
        symbol = symbols.get(currency, currency)
        return f"{symbol}{amount:.2f}"

    assert format_currency(99.5) == "$99.50"
    assert format_currency(150, "EUR") == "€150.00"


@qase.layer("api")
def test_api_response_structure():
    """API test - testing API response format."""
    response = {
        "status": "success",
        "data": {"id": 1, "name": "Test"},
        "meta": {"page": 1, "total": 100}
    }

    assert "status" in response
    assert "data" in response
    assert response["status"] == "success"


@qase.layer("e2e")
def test_user_registration_flow():
    """E2E test - testing complete user flow."""
    # Step 1: Fill registration form
    form_data = {"email": "new@example.com", "password": "SecureP@ss1"}

    # Step 2: Submit form
    submission_result = "success"

    # Step 3: Verify email sent
    email_sent = True

    # Step 4: Confirm email
    email_confirmed = True

    # Step 5: User can login
    login_successful = True

    assert all([
        submission_result == "success",
        email_sent,
        email_confirmed,
        login_successful
    ]), "Complete registration flow should work"


# ============================================================================
# @qase.fields - Multiple fields at once
# ============================================================================

@qase.id(10)
@qase.fields(
    ("severity", "critical"),
    ("priority", "high"),
    ("layer", "e2e"),
    ("description", "Complete checkout flow including cart, payment, and confirmation"),
    ("preconditions", "User must be logged in with items in cart"),
    ("postconditions", "Order should be created and confirmation email sent"),
)
def test_complete_checkout_flow():
    """Test with all metadata fields set using @qase.fields decorator."""
    # Cart validation
    cart = {"items": [{"id": 1, "qty": 2}], "total": 199.98}
    assert len(cart["items"]) > 0, "Cart should have items"

    # Payment processing
    payment_result = {"status": "approved", "transaction_id": "TXN123"}
    assert payment_result["status"] == "approved", "Payment should be approved"

    # Order creation
    order = {"id": "ORD-001", "status": "confirmed"}
    assert order["status"] == "confirmed", "Order should be confirmed"

    # Email confirmation
    email_sent = True
    assert email_sent, "Confirmation email should be sent"


# ============================================================================
# @qase.ignore - Exclude test from Qase reporting
# ============================================================================

@qase.ignore
def test_local_development_only():
    """This test is excluded from Qase reporting.

    Useful for tests that are:
    - Only for local development
    - Work in progress
    - Environment-specific debugging
    """
    debug_mode = True
    assert debug_mode, "This test runs locally but won't be reported to Qase"


# ============================================================================
# @qase.suite - Organize tests into suites
# ============================================================================

@qase.suite("Authentication")
def test_login_with_remember_me():
    """Test organized under 'Authentication' suite."""
    remember_me = True
    session_duration = 30 if remember_me else 1  # days

    assert session_duration == 30, "Remember me should extend session"


@qase.suite("Authentication", "OAuth")
def test_google_oauth_login():
    """Test organized under 'Authentication > OAuth' nested suite."""
    oauth_provider = "google"
    oauth_token = "valid_token"

    assert oauth_provider == "google"
    assert oauth_token is not None


@qase.suite("Authentication", "OAuth", "Error Handling")
def test_oauth_token_expiration():
    """Test organized under deeply nested suite structure."""
    token_expired = True
    refresh_successful = True

    if token_expired:
        assert refresh_successful, "Token refresh should work"
