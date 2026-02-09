# Attachments in Pytest

This guide covers how to attach files, screenshots, logs, and other content to your Qase test results.

---

## Overview

Qase Pytest Reporter supports attaching various types of content to test results:

- **Files** — Attach files from the filesystem
- **Screenshots** — Attach images captured during test execution
- **Logs** — Attach text logs or console output
- **Binary data** — Attach any binary content from memory

Attachments appear in the test result details in Qase TestOps.

---

## Attaching Files

### From File Path

```python
from qase.pytest import qase

def test_with_file_attachment():
    qase.attach("/path/to/screenshot.png")
    qase.attach("/path/to/test-data.json")
    assert True
```

### Multiple Files

```python
from qase.pytest import qase

def test_with_multiple_files():
    qase.attach(
        "/path/to/file1.txt",
        "/path/to/file2.txt",
        "/path/to/file3.txt"
    )
    assert True
```

### With Custom MIME Type

```python
from qase.pytest import qase

def test_with_mime_types():
    qase.attach(
        ("/path/to/data.json", "application/json"),
        ("/path/to/report.xml", "application/xml"),
    )
    assert True
```

---

## Attaching Content from Memory

### Text Content

```python
from qase.pytest import qase

def test_with_text_content():
    log_content = "Step 1: Started\nStep 2: Completed\nStep 3: Verified"
    qase.attach((log_content, "text/plain", "execution.log"))
    assert True
```

### Binary Content (Screenshots)

```python
from qase.pytest import qase

def test_with_screenshot(browser):
    # Capture screenshot as bytes
    screenshot_bytes = browser.screenshot()

    # Attach with filename
    qase.attach((screenshot_bytes, "image/png", "screenshot.png"))
    assert True
```

### JSON Data

```python
import json
from qase.pytest import qase

def test_with_json_data():
    data = {"user": "test", "result": "success", "items": [1, 2, 3]}
    json_str = json.dumps(data, indent=2)
    qase.attach((json_str, "application/json", "response.json"))
    assert True
```

---

## Attachments in Fixtures

### Attach on Teardown

```python
import pytest
from qase.pytest import qase

@pytest.fixture
def browser():
    driver = create_webdriver()
    yield driver

    # Attach screenshot regardless of test outcome
    screenshot = driver.get_screenshot_as_png()
    qase.attach((screenshot, "image/png", "final_state.png"))

    # Attach browser logs
    logs = driver.get_log('browser')
    log_text = '\n'.join(str(entry) for entry in logs)
    qase.attach((log_text, "text/plain", "browser.log"))

    driver.quit()
```

### Attach Only on Failure

```python
import pytest
from qase.pytest import qase

@pytest.fixture
def browser(request):
    driver = create_webdriver()
    yield driver

    # Attach screenshot only if test failed
    if request.node.rep_call.failed:
        screenshot = driver.get_screenshot_as_png()
        qase.attach((screenshot, "image/png", "failure_screenshot.png"))

    driver.quit()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)
```

---

## Method Reference

### `qase.attach()`

Attach content to the test case.

**Signatures:**

```python
# Single file path
qase.attach("/path/to/file")

# Multiple file paths
qase.attach("/path/to/file1", "/path/to/file2")

# File with MIME type
qase.attach(("/path/to/file", "mime/type"))

# Content from memory
qase.attach((content, "mime/type", "filename"))
```

**Parameters:**

| Format | Description |
|--------|-------------|
| `str` | File path (MIME type auto-detected) |
| `(str, str)` | (file_path, mime_type) |
| `(bytes\|str, str, str)` | (content, mime_type, filename) |

---

## MIME Types

Common MIME types are auto-detected based on file extension:

| Extension | MIME Type |
|-----------|-----------|
| `.png` | `image/png` |
| `.jpg`, `.jpeg` | `image/jpeg` |
| `.gif` | `image/gif` |
| `.svg` | `image/svg+xml` |
| `.webp` | `image/webp` |
| `.txt` | `text/plain` |
| `.log` | `text/plain` |
| `.json` | `application/json` |
| `.xml` | `application/xml` |
| `.html` | `text/html` |
| `.csv` | `text/csv` |
| `.pdf` | `application/pdf` |
| `.zip` | `application/zip` |

For other file types, specify MIME type explicitly.

---

## Common Use Cases

### Selenium Screenshots

```python
from selenium import webdriver
from qase.pytest import qase

def test_with_selenium(selenium_driver):
    selenium_driver.get("https://example.com")

    # Take screenshot
    screenshot = selenium_driver.get_screenshot_as_png()
    qase.attach((screenshot, "image/png", "page.png"))

    # Full page screenshot (if supported)
    selenium_driver.save_screenshot("/tmp/full_page.png")
    qase.attach("/tmp/full_page.png")

    assert selenium_driver.title == "Example Domain"
```

### Playwright Screenshots

```python
from qase.pytest import qase

def test_with_playwright(page):
    page.goto("https://example.com")

    # Screenshot as bytes
    screenshot = page.screenshot()
    qase.attach((screenshot, "image/png", "playwright_screenshot.png"))

    # Screenshot of specific element
    element_screenshot = page.locator("#main").screenshot()
    qase.attach((element_screenshot, "image/png", "element.png"))

    assert page.title() == "Example Domain"
```

### API Response Logs

```python
import requests
import json
from qase.pytest import qase

def test_api_response():
    response = requests.get("https://api.example.com/users")

    # Attach response body
    qase.attach((
        json.dumps(response.json(), indent=2),
        "application/json",
        "response.json"
    ))

    # Attach response headers
    headers_text = '\n'.join(f"{k}: {v}" for k, v in response.headers.items())
    qase.attach((headers_text, "text/plain", "headers.txt"))

    assert response.status_code == 200
```

### Browser Console Logs

```python
from qase.pytest import qase

def test_with_console_logs(browser):
    browser.goto("https://example.com")

    # Get console logs (browser-specific)
    console_logs = browser.get_console_logs()
    log_text = '\n'.join(str(log) for log in console_logs)
    qase.attach((log_text, "text/plain", "console.log"))

    assert True
```

### HAR Files (Network Traffic)

```python
from qase.pytest import qase

def test_with_har(page, context):
    # Start HAR recording
    context.tracing.start(screenshots=True, snapshots=True)

    page.goto("https://example.com")

    # Stop and save
    context.tracing.stop(path="trace.zip")
    qase.attach("trace.zip")

    assert True
```

---

## Troubleshooting

### Attachments Not Appearing

1. Verify the file path exists and is readable
2. Check file permissions
3. Enable debug logging:
   ```json
   {
     "debug": true
   }
   ```
4. Check console output for upload errors

### Large Files

Large attachments may slow down test execution. Consider:
- Compressing files before attaching
- Limiting screenshot resolution
- Only attaching on failure
- Setting reasonable size limits in your tests

### Binary Data Issues

When attaching binary data:
- Always provide a filename with appropriate extension
- Specify the correct MIME type
- Ensure content is bytes, not string (for binary data)

```python
# Correct
qase.attach((binary_data, "image/png", "screenshot.png"))

# Incorrect - missing filename
qase.attach((binary_data, "image/png"))
```

---

## See Also

- [Usage Guide](usage.md)
- [Steps Guide](STEPS.md)
- [Configuration Reference](../../qase-python-commons/README.md)
