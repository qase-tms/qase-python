import json
import os

from behave import given, when, then

from qase.behave import qase


@given("a passing condition")
def step_passing(context):
    assert True


@given("a failing condition")
def step_failing(context):
    assert False, "Intentional failure"


@given("a skipped condition")
def step_skipped(context):
    context.scenario.skip("Skipped for integration testing")


@given("a user opens the app")
def step_open_app(context):
    context.app_opened = True
    assert context.app_opened


@when("the user performs an action")
def step_perform_action(context):
    context.action_done = True
    assert context.action_done


@when("the user triggers a failure")
def step_trigger_failure(context):
    assert False, "Step failure"


@then("the result is verified")
def step_verify_result(context):
    assert True


@given("the first number is {a:d}")
def step_first_number(context, a):
    context.a = a


@given("the second number is {b:d}")
def step_second_number(context, b):
    context.b = b


@then("the sum is {result:d}")
def step_sum(context, result):
    assert context.a + context.b == result


@given("I attach a sample file")
def step_attach_file(context):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    attachments_dir = os.path.join(current_dir, "..", "..", "attachments")
    qase.attach(file_path=os.path.join(attachments_dir, "sample.txt"))
    assert True


@given("I attach content as json")
def step_attach_content(context):
    content = json.dumps({"key": "value"}, indent=2)
    qase.attach(content=content, file_name="data.json", mime_type="application/json")
    assert True
