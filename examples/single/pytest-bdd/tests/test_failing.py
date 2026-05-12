from pytest_bdd import scenarios, given, when, then

scenarios("../features/failing.feature")


@given("a calculator")
def a_calc():
    pass


@when("I add 2 and 2")
def add():
    pass


@then("the result should be 5")
def assert_five():
    assert 2 + 2 == 5
