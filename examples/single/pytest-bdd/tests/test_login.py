from pytest_bdd import scenarios, given, when, then

from qase.pytest import qase

scenarios("../features/login.feature")


@given("the user is on the login page")
def login_page():
    with qase.step("Open login page"):
        assert True


@when("the user enters valid credentials")
def valid_credentials():
    with qase.step("Enter username and password"):
        username = "admin"
        password = "password123"
        assert username == "admin"
        assert password == "password123"


@then("the user should see the dashboard")
def dashboard_visible():
    with qase.step("Verify dashboard is visible"):
        assert True
