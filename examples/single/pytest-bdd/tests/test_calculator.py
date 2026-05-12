from pytest_bdd import scenarios, given, then, parsers

scenarios("../features/calculator.feature")


@given(parsers.parse("I have {a:d} and {b:d}"), target_fixture="numbers")
def numbers(a, b):
    return a, b


@then(parsers.parse("their sum is {c:d}"))
def check_sum(numbers, c):
    assert sum(numbers) == c
