# Pytest Examples

Examples demonstrating Qase Pytest Reporter features.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure credentials in `qase.config.json`:
   - Replace `<token>` with your [API token](https://app.qase.io/user/api/token)
   - Replace `<project_code>` with your project code

   Or use environment variables:
   ```bash
   export QASE_TESTOPS_API_TOKEN=your_token
   export QASE_TESTOPS_PROJECT=your_project_code
   ```

## Run Tests

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_basic.py

# Run with verbose output
pytest tests/ -v
```

## Examples

| File | Description |
|------|-------------|
| `test_basic.py` | Decorators: `@qase.id`, `@qase.title`, `@qase.fields`, `@qase.description`, `@qase.priority`, `@qase.severity`, `@qase.layer`, `@qase.preconditions`, `@qase.postconditions` |
| `test_attachments.py` | Attachments: `qase.attach()` with files, bytes, and in steps |
| `test_steps.py` | Steps: `@qase.step` decorator and `with qase.step()` context manager |
| `test_sqlite_profiler.py` | Database profiling: SQLite operations with step tracking |
| `test_postgres_profiler.py` | Database profiling: PostgreSQL operations |
| `test_mysql_profiler.py` | Database profiling: MySQL operations |
| `test_mongodb_profiler.py` | Database profiling: MongoDB operations |
| `test_redis_profiler.py` | Database profiling: Redis operations |

## Code Examples

### Link to Test Case

```python
from qase.pytest import qase

@qase.id(1)
def test_with_id():
    assert True

@qase.id([1, 2, 3])  # Link to multiple test cases
def test_with_multiple_ids():
    assert True
```

### Add Metadata

```python
@qase.title("Login test")
@qase.description("Verify user can login with valid credentials")
@qase.severity("critical")
@qase.priority("high")
@qase.layer("e2e")
def test_login():
    assert True

# Or use @qase.fields for multiple fields
@qase.fields(
    ("severity", "critical"),
    ("priority", "high"),
    ("layer", "e2e"),
)
def test_with_fields():
    assert True
```

### Add Attachments

```python
def test_with_attachment():
    # Attach file from filesystem
    qase.attach("/path/to/file.txt")

    # Attach multiple files
    qase.attach("/path/to/file1.txt", "/path/to/file2.png")

    # Attach with MIME type
    qase.attach(("/path/to/file.json", "application/json"))

    # Attach bytes data
    qase.attach((b"test data", "text/plain", "data.txt"))

    assert True
```

### Add Steps

```python
@qase.step("Step as decorator")
def helper_function():
    pass

def test_with_steps():
    helper_function()

    with qase.step("Step as context manager"):
        # step code here
        pass

    assert True
```

## Profiler Examples

The `test_*_profiler.py` files demonstrate database profiling with automatic step tracking. Enable profiling in `qase.config.json`:

```json
{
  "profilers": ["db"],
  "framework": {
    "pytest": {
      "capture": {
        "logs": true,
        "http": true
      }
    }
  }
}
```

## Documentation

- [Pytest Reporter README](../../../qase-pytest/README.md)
- [Usage Guide](../../../qase-pytest/docs/usage.md)
- [Configuration Reference](../../../qase-python-commons/README.md)
