# qase-behave 1.1.3

## What's new

- Added support for file and content attachments to test results using `qase.attach()` method.
- Added support for adding comments to test results using `qase.comment()` method.
- Improved MIME type detection for attachments.
- Updated documentation with examples and usage instructions.

### Attachment Usage

```python
from qase.behave import qase

# Attach a file
qase.attach(file_path="/path/to/file.txt")

# Attach content directly
qase.attach(content="test data", file_name="data.txt")

# Attach binary data
qase.attach(content=b"binary data", file_name="screenshot.png", mime_type="image/png")
```

### Comment Usage

```python
from qase.behave import qase

# Add comments to test results
qase.comment("Test completed successfully")
qase.comment("Debug info: user logged in")
```

# qase-behave 1.1.2

## What's new

- Fixed an issue with the start time of the step execution.

# qase-behave 1.1.1

## What's new

- Added support for test run tags.
- Added support for excluding parameters from test results.

# qase-behave 1.1.0

## What's new

- Updated core package to the latest supported versions.
- Improved logic for handling multiple QaseID values in test results.
- Removed `useV2` configuration option. The reporter now always uses API v2 for sending results.

# qase-behave 1.0.3

## What's new

- Logging of host system details to improve debugging and traceability.  
- Output of installed packages in logs for better environment visibility.  

# qase-behave 1.0.2

## What's new

Added support for specifying multiple test case IDs for a single automated test, improving test case association and
traceability.

```gherkin
@qase.id:2,3,4
Scenario: Test with QaseID
```
# qase-behave 1.0.1

## What's new

Resolved an issue where tests marked with the `qase.ignore` tag were still being submitted to Qase.

# qase-behave 1.0.0

## What's new

The first release in the 1.0.x series of the Behave reporter.
