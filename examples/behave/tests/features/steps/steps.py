from behave import *

@given('I have a simple test')
def step_impl(context):
    pass

@given('I have a test with parameters "{param1}" and "{param2}"')
def step_given_test_with_parameters(context, param1, param2):
    pass

@when('I run it')
def step_impl(context):
    pass


@then('it should pass')
def step_impl(context):
    pass


@then('it should fail')
def step_impl(context):
    assert False
