from behave import *
from qase.behave import qase
import tempfile
import os


@given('I have a test with attachments')
def step_impl(context):
    # Create a temporary file for testing
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write("This is a test attachment content")
        context.temp_file_path = f.name



@when('I attach a file to the test')
def step_impl(context):
    # Attach the temporary file
    qase.attach(file_path=context.temp_file_path)


@when('I attach content as text')
def step_impl(context):
    # Attach text content directly
    qase.attach(content="This is some text content", file_name="text_content.txt")


@when('I attach JSON data')
def step_impl(context):
    # Attach JSON content
    json_data = '{"test": "data", "value": 123}'
    qase.attach(content=json_data, file_name="test_data.json", mime_type="application/json")


@then('the attachments should be included in the test result')
def step_impl(context):
    # # Clean up temporary file
    if hasattr(context, 'temp_file_path') and os.path.exists(context.temp_file_path):
        os.unlink(context.temp_file_path)



@given('I want to attach a screenshot')
def step_impl(context):
    # Simulate creating a screenshot (in real scenario, this would be actual screenshot data)
    context.screenshot_data = b"fake_screenshot_data"
    pass


@when('I attach the screenshot')
def step_impl(context):
    # Attach binary data (screenshot)
    qase.attach(
        content=context.screenshot_data,
        file_name="screenshot.png",
        mime_type="image/png"
    )


@when('I add a comment about the test')
def step_impl(context):
    # Add a comment to the test result
    qase.comment("Screenshot captured successfully")
    qase.comment("User was logged in at the time of capture")


@when('I add debug information')
def step_impl(context):
    # Add debug information as comments
    import datetime
    qase.comment(f"Debug: Current timestamp is {datetime.datetime.now()}")
    qase.comment("Debug: All elements were found and interacted with")
