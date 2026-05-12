from pytest_bdd import scenarios, given, when, then

scenarios("../features/data_carriers.feature")


@given("the following users:")
def users(datatable=None):
    # pytest-bdd injects the data table into the step function when a
    # parameter named `datatable` is present; ignore it here — the
    # purpose of this example is to see the table land in the Qase report.
    pass


@when("I send the payload:")
def payload(docstring=None):
    pass


@then("the request succeeds")
def request_ok():
    assert True
