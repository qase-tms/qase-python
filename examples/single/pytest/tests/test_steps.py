"""
Step tracking examples demonstrating Qase Pytest Reporter step functionality.

Steps are used to break down test execution into logical phases,
making test results more readable and easier to debug in Qase.
"""
from qase.pytest import qase


# ============================================================================
# @qase.step decorator - Reusable step functions
# ============================================================================

@qase.step("Open the application home page")
def open_home_page():
    """Simulates opening the application."""
    app_loaded = True
    return {"url": "https://app.example.com", "loaded": app_loaded}


@qase.step("Enter login credentials")
def enter_credentials(username: str, password: str):
    """Simulates entering login credentials."""
    return {"username": username, "password_length": len(password)}


@qase.step("Click the login button")
def click_login_button():
    """Simulates clicking the login button."""
    return {"clicked": True, "timestamp": "2024-01-15T10:30:00Z"}


@qase.step("Verify user dashboard is displayed")
def verify_dashboard(expected_user: str):
    """Simulates verifying the dashboard."""
    dashboard = {
        "visible": True,
        "username_displayed": expected_user,
        "widgets_loaded": 5
    }
    assert dashboard["visible"], "Dashboard should be visible"
    return dashboard


def test_login_flow_with_step_decorator():
    """Demonstrates using @qase.step decorator for reusable steps."""
    # Step 1: Open home page
    home = open_home_page()
    assert home["loaded"], "Home page should load"

    # Step 2: Enter credentials
    creds = enter_credentials("admin@example.com", "SecurePass123!")
    assert creds["username"] == "admin@example.com"

    # Step 3: Click login
    click_result = click_login_button()
    assert click_result["clicked"], "Login button should be clicked"

    # Step 4: Verify dashboard
    dashboard = verify_dashboard("admin@example.com")
    assert dashboard["widgets_loaded"] > 0, "Dashboard should have widgets"


# ============================================================================
# with qase.step() context manager - Inline steps
# ============================================================================

def test_checkout_flow_with_context_manager():
    """Demonstrates using 'with qase.step()' for inline step definitions."""
    cart_items = []
    order = {}

    with qase.step("Add products to shopping cart"):
        cart_items.append({"id": 1, "name": "Wireless Mouse", "price": 29.99})
        cart_items.append({"id": 2, "name": "USB-C Hub", "price": 49.99})
        assert len(cart_items) == 2, "Cart should have 2 items"

    with qase.step("Apply discount coupon"):
        coupon = "SAVE10"
        discount_percent = 10
        subtotal = sum(item["price"] for item in cart_items)
        discount_amount = subtotal * (discount_percent / 100)
        total = subtotal - discount_amount
        assert discount_amount > 0, "Discount should be applied"

    with qase.step("Enter shipping information"):
        shipping = {
            "name": "John Doe",
            "address": "123 Main St",
            "city": "San Francisco",
            "zip": "94105",
            "country": "USA"
        }
        shipping_valid = all(shipping.values())
        assert shipping_valid, "All shipping fields should be filled"

    with qase.step("Process payment"):
        payment = {
            "method": "credit_card",
            "card_last_four": "4242",
            "amount": total,
            "status": "approved"
        }
        assert payment["status"] == "approved", "Payment should be approved"

    with qase.step("Confirm order creation"):
        order = {
            "id": "ORD-2024-001",
            "items": cart_items,
            "shipping": shipping,
            "payment": payment,
            "status": "confirmed"
        }
        assert order["status"] == "confirmed", "Order should be confirmed"


# ============================================================================
# Nested steps - Steps within steps
# ============================================================================

@qase.step("Validate user registration form")
def validate_registration_form(form_data: dict):
    """Parent step containing nested validation steps."""

    @qase.step("Validate email format")
    def validate_email(email: str) -> bool:
        return "@" in email and "." in email.split("@")[1]

    @qase.step("Validate password strength")
    def validate_password(password: str) -> dict:
        return {
            "length_ok": len(password) >= 8,
            "has_upper": any(c.isupper() for c in password),
            "has_lower": any(c.islower() for c in password),
            "has_digit": any(c.isdigit() for c in password),
        }

    @qase.step("Validate required fields")
    def validate_required(data: dict, required: list) -> bool:
        return all(data.get(field) for field in required)

    email_valid = validate_email(form_data.get("email", ""))
    password_check = validate_password(form_data.get("password", ""))
    required_valid = validate_required(form_data, ["email", "password", "name"])

    return {
        "email_valid": email_valid,
        "password_valid": all(password_check.values()),
        "required_valid": required_valid,
        "overall_valid": email_valid and all(password_check.values()) and required_valid
    }


def test_registration_with_nested_steps():
    """Demonstrates nested steps - steps that contain other steps."""
    form_data = {
        "email": "newuser@example.com",
        "password": "SecureP@ss123",
        "name": "John Doe"
    }

    with qase.step("User fills registration form"):
        # Form data is already prepared above
        assert form_data["email"], "Email should be filled"

    validation = validate_registration_form(form_data)
    assert validation["overall_valid"], "Form should be valid"

    with qase.step("Submit registration"):
        submission_result = {"success": True, "user_id": 12345}
        assert submission_result["success"], "Registration should succeed"


# ============================================================================
# Steps with expected results and data
# ============================================================================

@qase.step("Fetch user profile from API")
def fetch_user_profile(user_id: int) -> dict:
    """Step that returns data for verification."""
    # Simulated API response
    return {
        "id": user_id,
        "name": "Jane Smith",
        "email": "jane.smith@example.com",
        "role": "admin",
        "created_at": "2023-01-15",
        "last_login": "2024-01-14"
    }


@qase.step("Update user profile")
def update_user_profile(user_id: int, updates: dict) -> dict:
    """Step that performs an update operation."""
    # Simulated update result
    return {
        "success": True,
        "updated_fields": list(updates.keys()),
        "new_values": updates
    }


@qase.step("Verify profile changes")
def verify_profile_changes(original: dict, updated: dict, expected_changes: dict) -> bool:
    """Step that verifies expected changes were applied."""
    for field, expected_value in expected_changes.items():
        if updated.get(field) != expected_value:
            return False
    return True


def test_user_profile_update_flow():
    """Demonstrates steps with data flow and verification."""
    user_id = 42

    # Step 1: Get current profile
    original_profile = fetch_user_profile(user_id)
    assert original_profile["id"] == user_id

    # Step 2: Prepare and apply updates
    profile_updates = {
        "name": "Jane Doe",
        "role": "super_admin"
    }
    update_result = update_user_profile(user_id, profile_updates)
    assert update_result["success"], "Update should succeed"

    # Step 3: Fetch updated profile
    with qase.step("Fetch updated profile"):
        updated_profile = {**original_profile, **profile_updates}

    # Step 4: Verify changes
    changes_verified = verify_profile_changes(
        original_profile,
        updated_profile,
        profile_updates
    )
    assert changes_verified, "All changes should be verified"


# ============================================================================
# Combined patterns - Complex test with mixed step styles
# ============================================================================

@qase.step("Initialize test database")
def init_test_database():
    """Setup step for database."""
    return {"connection": "active", "tables_created": True}


@qase.step("Create test user")
def create_test_user(db, user_data: dict):
    """Step to create a user in database."""
    return {"id": 1, **user_data, "created": True}


@qase.step("Clean up test data")
def cleanup_test_data(db, user_id: int):
    """Teardown step to clean up."""
    return {"deleted": True, "user_id": user_id}


@qase.id(100)
@qase.title("Complete E2E user management flow")
@qase.severity("critical")
def test_e2e_user_management():
    """Complex test demonstrating all step patterns combined."""
    user_id = None

    # Setup phase
    db = init_test_database()
    assert db["connection"] == "active"

    try:
        # Create phase
        user = create_test_user(db, {
            "name": "Test User",
            "email": "test@example.com"
        })
        user_id = user["id"]
        assert user["created"]

        # Verification phase with inline steps
        with qase.step("Verify user exists in database"):
            user_exists = True  # Simulated check
            assert user_exists, "User should exist"

        with qase.step("Verify user can authenticate"):
            auth_result = {"success": True, "token": "xyz123"}
            assert auth_result["success"], "User should be able to authenticate"

        with qase.step("Verify user permissions"):
            permissions = ["read", "write"]
            assert "read" in permissions, "User should have read permission"

    finally:
        # Cleanup phase
        if user_id:
            cleanup_result = cleanup_test_data(db, user_id)
            assert cleanup_result["deleted"]
