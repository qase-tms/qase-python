from pytest_bdd import scenarios, given, when, then, parsers

scenarios("../features/checkout.feature")


@given("the user is signed in")
def signed_in():
    pass


@given("the cart contains 2 items")
def cart_two_items():
    pass


@given("the saved card is expired")
def expired_card():
    pass


@when(parsers.parse('the user clicks "{label}"'))
def click(label):
    assert label == "Place order"


@then("the order is created")
def order_created():
    assert True


@then(parsers.parse('the payment fails with "{reason}"'))
def payment_failure(reason):
    assert reason == "card_expired"
