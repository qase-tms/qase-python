# Qase Pre-commit Hooks

Pre-commit hooks for Qase Python projects to ensure code quality and consistency.

## Installation

Add to your `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/qase-tms/qase-python
    rev: qase-hooks-v0.1.0  # Use the tag or branch you want
    hooks:
      - id: qase-id-check
```

Then run:

```bash
pre-commit install
pre-commit autoupdate  # To update to the latest version
```

## Available Hooks

### qase-id-check

Scans pytest test files and ensures all test functions and test methods have either a `@qase.id()` decorator or `@qase.ignore()` decorator.

**Features:**

- Scans staged Python files that look like pytest test modules
- Detects test functions (starting with `test_`) and test methods in test classes
- Checks for `@qase.id(...)` or `@qase.ignore()` decorators
- Blocks the commit by default if tests are missing decorators
- Supports `--warn` mode for warnings only
- Supports `--exclude` for ignoring specific files/patterns

**What files are checked:**

The hook only checks Python files that match pytest test file patterns:

- Files starting with `test_` (e.g., `test_users.py`)
- Files ending with `_test.py` (e.g., `users_test.py`)
- Files starting with `test` and ending with `.py` (e.g., `test.py`)

**What it checks:**

- Test functions starting with `test_` (e.g., `test_user_login`)
- Test methods in classes starting with `Test` (e.g., `TestUserAPI.test_create_user`)

**Valid decorators:**

- `@qase.id(1)` - Single Qase ID
- `@qase.id([1, 2, 3])` - Multiple Qase IDs
- `@qase.ignore()` - Explicitly ignore the test in Qase

**Test classes example:**

The hook also checks test methods in test classes:

```python
class TestUserAPI:
    @qase.id(1)
    def test_create_user(self):
        pass
```

## Configuration Options

### Default Behavior (Block Commit)

By default, the hook blocks the commit if any test is missing `@qase.id()` or `@qase.ignore()` decorator:

```yaml
repos:
  - repo: https://github.com/qase-tms/qase-python
    rev: qase-hooks-v0.1.0
    hooks:
      - id: qase-id-check
        # No args - blocks commit by default
```

### Warning Mode

Only warns about missing decorators but allows the commit to proceed:

```yaml
repos:
  - repo: https://github.com/qase-tms/qase-python
    rev: qase-hooks-v0.1.0
    hooks:
      - id: qase-id-check
        args: [--warn]
```

### Excluding Files

Exclude specific files or patterns from checking:

```yaml
repos:
  - repo: https://github.com/qase-tms/qase-python
    rev: qase-hooks-v0.1.0
    hooks:
      - id: qase-id-check
        args: [--exclude, "test_legacy", --exclude, "old_tests"]
```

Or combine with warning mode:

```yaml
repos:
  - repo: https://github.com/qase-tms/qase-python
    rev: qase-hooks-v0.1.0
    hooks:
      - id: qase-id-check
        args: [--warn, --exclude, "test_legacy"]
```

## Example Output

### Default Mode (Block Commit)

```
Tests without qase.id() decorator found:
  tests/api/test_users.py:42  → test_get_users_without_id
  tests/api/test_users.py:55  → TestUserAPI.test_create_user

Please add @qase.id(...) or @qase.ignore() to these tests.
```

### Warning Mode

```
Tests without qase.id() decorator found:
  tests/api/test_users.py:42  → test_get_users_without_id

(Warning only - commit will proceed)
```
