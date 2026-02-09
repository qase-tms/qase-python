"""
Step definitions for Behave examples.

These steps demonstrate realistic test scenarios while remaining
simple enough to run without external dependencies.
"""
from behave import given, when, then


# ============================================================================
# User Authentication Steps
# ============================================================================

@given('a registered user exists with email "{email}"')
def step_user_exists(context, email):
    context.user = {"email": email, "password": "SecurePass123"}


@given('the user is logged in')
def step_user_logged_in(context):
    context.session = {"active": True, "user_id": 1}


@given('the login page is displayed')
def step_login_page(context):
    context.current_page = "login"


@when('the user enters valid credentials')
def step_enter_valid_creds(context):
    context.login_attempt = {"valid": True}


@when('the user enters wrong password')
def step_enter_wrong_password(context):
    context.login_attempt = {"valid": False, "error": "Invalid password"}


@when('user enters valid credentials')
def step_user_enters_valid_creds(context):
    context.login_attempt = {"valid": True}


@when('user enters email "{email}"')
def step_enter_email(context, email):
    context.entered_email = email


@when('user enters password "{password}"')
def step_enter_password(context, password):
    context.entered_password = password


@when('clicks the login button')
def step_click_login(context):
    context.login_submitted = True


@when('clicks submit button')
def step_click_submit(context):
    context.form_submitted = True


@when('the user clicks logout')
def step_click_logout(context):
    context.session = {"active": False}


@then('the user should be redirected to dashboard')
def step_redirect_dashboard(context):
    assert context.login_attempt.get("valid", False), "Login should be valid"


@then('should see welcome message')
def step_see_welcome(context):
    pass  # Verified by UI in real scenario


@then('an error message should be displayed')
def step_error_displayed(context):
    assert not context.login_attempt.get("valid", True), "Should have error"


@then('the user should remain on login page')
def step_remain_login(context):
    pass


@then('the session should be terminated')
def step_session_terminated(context):
    assert not context.session.get("active", True)


@then('the user should be redirected to login page')
def step_redirect_login(context):
    pass


@then('user should be authenticated')
def step_user_authenticated(context):
    pass


@then('redirected to dashboard')
def step_redirected_dashboard(context):
    pass


# ============================================================================
# OAuth Steps
# ============================================================================

@when('user clicks "{button_text}"')
def step_click_button(context, button_text):
    context.clicked_button = button_text


@when('completes Google authentication')
def step_google_auth(context):
    context.oauth_result = {"provider": "google", "success": True}


@when('completes GitHub authentication')
def step_github_auth(context):
    context.oauth_result = {"provider": "github", "success": True}


@when('Google returns authentication error')
def step_google_error(context):
    context.oauth_result = {"provider": "google", "success": False, "error": "Access denied"}


@then('profile should be synced from Google')
def step_profile_google(context):
    assert context.oauth_result.get("provider") == "google"


@then('profile should be synced from GitHub')
def step_profile_github(context):
    assert context.oauth_result.get("provider") == "github"


@then('error message should be displayed')
def step_error_message(context):
    assert context.oauth_result.get("error") is not None


# ============================================================================
# Session and Security Steps
# ============================================================================

@when('checks "remember me" checkbox')
def step_check_remember_me(context):
    context.remember_me = True


@then('session should persist for 30 days')
def step_session_persist(context):
    assert context.remember_me


@given('user has account with email "{email}"')
def step_user_has_account(context, email):
    context.user_account = {"email": email, "locked": False, "failed_attempts": 0}


@when('user enters wrong password {count} times')
def step_wrong_password_times(context, count):
    context.user_account["failed_attempts"] = int(count)
    if int(count) >= 5:
        context.user_account["locked"] = True


@then('account should be locked')
def step_account_locked(context):
    assert context.user_account.get("locked", False)


@then('lockout notification email should be sent')
def step_lockout_email(context):
    pass  # Email sending verified separately


@given('user has 2FA enabled')
def step_2fa_enabled(context):
    context.two_factor = {"enabled": True}


@when('2FA code is requested')
def step_2fa_requested(context):
    context.two_factor["code_sent"] = True


@when('user enters valid 2FA code')
def step_enter_2fa(context):
    context.two_factor["verified"] = True


@given('user is inactive for 30 minutes')
def step_inactive(context):
    context.session["inactive_minutes"] = 30


@when('user performs an action')
def step_perform_action(context):
    if context.session.get("inactive_minutes", 0) >= 30:
        context.session["expired"] = True


@then('session should be expired')
def step_session_expired(context):
    assert context.session.get("expired", False)


@then('user should be redirected to login')
def step_redirect_to_login(context):
    pass


# ============================================================================
# Shopping Cart Steps
# ============================================================================

@given('a user has items in shopping cart')
def step_cart_items(context):
    context.cart = {"items": [{"id": 1, "price": 99.99}], "total": 99.99}


@given('valid payment method is configured')
def step_payment_configured(context):
    context.payment = {"method": "credit_card", "valid": True}


@given('the following items in cart:')
def step_items_table(context):
    context.cart = {"items": [], "total": 0}
    for row in context.table:
        item = {
            "name": row["name"],
            "price": float(row["price"]),
            "quantity": int(row["quantity"])
        }
        context.cart["items"].append(item)


@when('the user initiates checkout')
def step_init_checkout(context):
    context.checkout = {"initiated": True}


@when('confirms the payment')
def step_confirm_payment(context):
    context.checkout["payment_confirmed"] = True


@when('the cart total is calculated')
def step_calculate_total(context):
    total = sum(item["price"] * item["quantity"] for item in context.cart["items"])
    context.cart["total"] = round(total, 2)


@then('the order should be created')
def step_order_created(context):
    context.order = {"id": "ORD-001", "status": "created"}


@then('confirmation email should be sent')
def step_confirmation_email(context):
    pass


@then('the total should be {expected_total}')
def step_verify_total(context, expected_total):
    assert abs(context.cart["total"] - float(expected_total)) < 0.01


# ============================================================================
# Password Reset Steps
# ============================================================================

@given('user exists with email "{email}"')
def step_user_exists_email(context, email):
    context.reset_user = {"email": email}


@when('user requests password reset')
def step_request_reset(context):
    context.reset_requested = True


@then('reset email should be sent')
def step_reset_email_sent(context):
    assert context.reset_requested


@then('email should contain reset link')
def step_email_has_link(context):
    pass


# ============================================================================
# Search Steps
# ============================================================================

@given('products exist in the catalog')
def step_products_exist(context):
    context.catalog = ["Laptop", "Desktop", "Tablet", "Phone"]


@when('user searches for "{query}"')
def step_search(context, query):
    context.search_results = [p for p in context.catalog if query.lower() in p.lower()]


@then('search results should contain "{expected}"')
def step_results_contain(context, expected):
    assert any(expected.lower() in r.lower() for r in context.search_results)


@then('results should be sorted by relevance')
def step_sorted_relevance(context):
    pass  # Sorting verified separately


# ============================================================================
# Profile Steps
# ============================================================================

@given('viewing profile page')
def step_view_profile(context):
    context.current_page = "profile"


@when('user updates their name to "{name}"')
def step_update_name(context, name):
    context.profile_update = {"name": name}


@when('saves the changes')
def step_save_changes(context):
    context.profile_update["saved"] = True


@then('profile should be updated successfully')
def step_profile_updated(context):
    assert context.profile_update.get("saved", False)


# ============================================================================
# Parametrized Test Steps
# ============================================================================

@given('user with role "{role}" exists')
def step_user_role(context, role):
    context.user = {"role": role}


@when('user logs in with email "{email}"')
def step_login_email(context, email):
    context.logged_in_email = email


@then('user should have access to "{pages}"')
def step_access_pages(context, pages):
    expected_pages = pages.split(",")
    # Simplified permission check
    assert len(expected_pages) > 0


@when('email "{email}" is validated')
def step_validate_email(context, email):
    is_valid = "@" in email and "." in email.split("@")[-1] if "@" in email else False
    has_local = email.split("@")[0] if "@" in email else ""
    has_domain = email.split("@")[-1] if "@" in email else ""

    if not is_valid or not has_local:
        context.validation = {"result": "invalid", "error": "Missing @ symbol" if "@" not in email else "Invalid format"}
    elif email.startswith("@"):
        context.validation = {"result": "invalid", "error": "Missing local part"}
    elif email.endswith("@"):
        context.validation = {"result": "invalid", "error": "Missing domain"}
    elif ".com" in email and email.split("@")[-1].startswith("."):
        context.validation = {"result": "invalid", "error": "Invalid domain format"}
    else:
        context.validation = {"result": "valid", "error": "none"}


@then('validation result should be "{result}"')
def step_validation_result(context, result):
    assert context.validation["result"] == result


@then('error message should be "{message}"')
def step_validation_error(context, message):
    assert context.validation["error"] == message


@given('API endpoint "{endpoint}" exists')
def step_api_endpoint(context, endpoint):
    context.api_endpoint = endpoint


@when('"{method}" request is sent')
def step_send_request(context, method):
    # Simulated API responses
    responses = {
        ("/api/users", "GET"): {"status": 200, "body": {"users": []}},
        ("/api/posts", "GET"): {"status": 200, "body": {"posts": []}},
        ("/api/invalid", "GET"): {"status": 404, "body": {"error": "Not found"}},
        ("/api/users", "POST"): {"status": 201, "body": {"id": 1}},
        ("/api/unauthorized", "POST"): {"status": 401, "body": {"error": "Unauthorized"}},
    }
    key = (context.api_endpoint, method)
    context.api_response = responses.get(key, {"status": 500, "body": {"error": "Unknown"}})


@then('response status should be {status_code:d}')
def step_status_code(context, status_code):
    assert context.api_response["status"] == status_code


@then('response should contain "{field}"')
def step_response_contains(context, field):
    assert field in context.api_response["body"]


@given('base price is {price}')
def step_base_price(context, price):
    context.pricing = {"base": float(price)}


@given('discount type is "{discount_type}"')
def step_discount_type(context, discount_type):
    context.pricing["type"] = discount_type


@given('discount value is {value}')
def step_discount_value(context, value):
    context.pricing["value"] = float(value)


@when('discount is applied')
def step_apply_discount(context):
    base = context.pricing["base"]
    value = context.pricing["value"]
    if context.pricing["type"] == "percentage":
        context.pricing["final"] = base - (base * value / 100)
    else:
        context.pricing["final"] = base - value


@then('final price should be {expected}')
def step_final_price(context, expected):
    assert abs(context.pricing["final"] - float(expected)) < 0.01


@when('password "{password}" is checked')
def step_check_password(context, password):
    length = len(password)
    if length < 8:
        context.password_check = {"valid": "invalid", "message": "Password must be at least 8 chars"}
    elif length > 32:
        context.password_check = {"valid": "invalid", "message": "Password exceeds 32 chars"}
    else:
        context.password_check = {"valid": "valid", "message": "Password meets requirements"}


@then('password should be "{validity}"')
def step_password_validity(context, validity):
    assert context.password_check["valid"] == validity


@then('message should be "{message}"')
def step_password_message(context, message):
    assert context.password_check["message"] == message
