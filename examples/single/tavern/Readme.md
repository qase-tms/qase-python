# Tavern Examples

Examples demonstrating Qase Tavern Reporter features.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure credentials:
   ```bash
   export QASE_MODE=testops
   export QASE_TESTOPS_API_TOKEN=your_token
   export QASE_TESTOPS_PROJECT=your_project_code
   ```

   Or edit `qase.config.json` and replace `<token>` and `<project_code>`.

## Run Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest test_simple.tavern.yaml

# Run with verbose output
pytest -v
```

## Examples

| File | Description |
|------|-------------|
| `test_simple.tavern.yaml` | Basic API tests without Qase IDs (auto-created test cases) |
| `test_with_id.tavern.yaml` | API tests linked to existing Qase test cases |

## Code Examples

### Basic Test (Auto-create)

```yaml
---
test_name: Get user list

stages:
  - name: Request users
    request:
      url: https://jsonplaceholder.typicode.com/users
      method: GET
    response:
      status_code: 200
```

### Link to Test Case

```yaml
---
test_name: QaseID=1 Get specific user

stages:
  - name: Request user by ID
    request:
      url: https://jsonplaceholder.typicode.com/users/1
      method: GET
    response:
      status_code: 200
      json:
        id: 1
```

### Multiple Test Cases

```yaml
---
test_name: QaseID=1,2 Test linked to multiple cases

stages:
  - name: Execute request
    request:
      url: https://api.example.com/endpoint
      method: GET
    response:
      status_code: 200
```

### Stages as Steps

Each stage in your Tavern test is automatically reported as a step in Qase:

```yaml
---
test_name: QaseID=5 Multi-step test

stages:
  - name: Step 1 - Create resource    # Reported as step 1
    request:
      url: https://api.example.com/resource
      method: POST
      json:
        name: test
    response:
      status_code: 201
      save:
        json:
          resource_id: id

  - name: Step 2 - Verify resource    # Reported as step 2
    request:
      url: https://api.example.com/resource/{resource_id}
      method: GET
    response:
      status_code: 200

  - name: Step 3 - Delete resource    # Reported as step 3
    request:
      url: https://api.example.com/resource/{resource_id}
      method: DELETE
    response:
      status_code: 204
```

## Documentation

- [Tavern Reporter README](../../../qase-tavern/README.md)
- [Usage Guide](../../../qase-tavern/docs/usage.md)
- [Configuration Reference](../../../qase-python-commons/README.md)
