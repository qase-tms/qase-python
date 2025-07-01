# Attachments in Qase Behave

Qase Behave supports attaching files and content to test results. This allows you to provide additional context for test failures, such as screenshots, logs, or data files.

## Usage

### Import the qase object

```python
from qase.behave import qase
```

### Attach a file

```python
@given('I have a test with a file')
def step_impl(context):
    # Attach an existing file
    qase.attach(file_path="/path/to/your/file.txt")
```

### Attach content directly

```python
@when('I attach text content')
def step_impl(context):
    # Attach text content
    qase.attach(content="This is some text content", file_name="content.txt")
```

### Attach binary data

```python
@when('I attach a screenshot')
def step_impl(context):
    # Attach binary data (e.g., screenshot)
    screenshot_data = b"binary_screenshot_data"
    qase.attach(
        content=screenshot_data,
        file_name="screenshot.png",
        mime_type="image/png"
    )
```

### Attach JSON data

```python
@when('I attach JSON data')
def step_impl(context):
    json_data = '{"test": "data", "value": 123}'
    qase.attach(
        content=json_data,
        file_name="test_data.json",
        mime_type="application/json"
    )
```

## Method Signature

```python
qase.attach(
    file_path: Optional[str] = None,
    content: Optional[Union[str, bytes]] = None,
    file_name: Optional[str] = None,
    mime_type: Optional[str] = None
) -> None
```

### Parameters

- **file_path**: Path to the file to attach (mutually exclusive with `content`)
- **content**: Content to attach as string or bytes (mutually exclusive with `file_path`)
- **file_name**: Name for the attachment (auto-detected from `file_path` if not provided)
- **mime_type**: MIME type of the attachment (auto-detected if not provided)

### Notes

- Either `file_path` or `content` must be provided, but not both
- If `file_name` is not provided, it will be derived from `file_path` or default to "attachment.txt"
- If `mime_type` is not provided, it will be auto-detected from the file extension or default to "text/plain"
- Attachments are automatically included in the test result when the scenario completes

## Examples

### Complete Example

```python
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

@when('I attach multiple items')
def step_impl(context):
    # Attach the temporary file
    qase.attach(file_path=context.temp_file_path)
    
    # Attach text content
    qase.attach(content="Additional text content", file_name="additional.txt")
    
    # Attach JSON data
    json_data = '{"status": "success", "timestamp": "2024-01-01T00:00:00Z"}'
    qase.attach(content=json_data, file_name="status.json", mime_type="application/json")

@then('clean up temporary files')
def step_impl(context):
    if hasattr(context, 'temp_file_path') and os.path.exists(context.temp_file_path):
        os.unlink(context.temp_file_path)
```

### Error Handling

The `qase.attach()` method will raise appropriate exceptions:

- `RuntimeError`: If called outside of an active scenario
- `ValueError`: If both `file_path` and `content` are provided, or if neither is provided
- `FileNotFoundError`: If the specified file path doesn't exist (when using `file_path`)

## Adding Comments

You can also add comments to your test scenarios using the `qase.comment()` method:

```python
@when('I add a comment')
def step_impl(context):
    qase.comment("This is a test comment")
    qase.comment("Another comment with additional context")
```

### Comment Method Signature

```python
qase.comment(message: str) -> None
```

### Parameters

- **message**: The comment message to add to the scenario

### Notes

- Comments are automatically included in the test result when the scenario completes
- Multiple comments are concatenated with newlines
- If no active scenario is available, a RuntimeError will be raised

## Integration with Qase TestOps

Attachments and comments added using `qase.attach()` and `qase.comment()` will be automatically uploaded to Qase TestOps when the test results are submitted. The attachments and comments will be associated with the corresponding test case and will be available in the Qase TestOps interface. 
