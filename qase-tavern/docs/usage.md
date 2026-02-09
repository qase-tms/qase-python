# Qase Integration in Tavern

This guide provides comprehensive instructions for integrating Qase with Tavern API testing framework.

> **Configuration:** For complete configuration reference including all available options, environment variables, and examples, see the [qase-python-commons README](../../qase-python-commons/README.md).

---

## Table of Contents

- [Adding QaseID](#adding-qaseid)
- [Test Stages as Steps](#test-stages-as-steps)
- [Multi-Project Support](#multi-project-support)
- [Running Tests](#running-tests)
- [Complete Examples](#complete-examples)

---

## Adding QaseID

Link your Tavern tests to existing test cases in Qase by adding `QaseID={ID}` to the test name.

### Single ID

```yaml
---
test_name: QaseID=1 Get user profile

stages:
  - name: Get user
    request:
      url: https://api.example.com/users/1
      method: GET
    response:
      status_code: 200
      json:
        id: 1
        name: "John Doe"
```

### Multiple IDs

Link one test to multiple test cases:

```yaml
---
test_name: QaseID=1,2,3 User authentication flow

stages:
  - name: Login
    request:
      url: https://api.example.com/auth/login
      method: POST
      json:
        username: testuser
        password: testpass
    response:
      status_code: 200
      save:
        json:
          token: token
```

### Test Without QaseID

Tests without `QaseID` are still reported to Qase but create new test cases:

```yaml
---
test_name: Simple health check

stages:
  - name: Check health endpoint
    request:
      url: https://api.example.com/health
      method: GET
    response:
      status_code: 200
```

### Multi-Project Support

To send test results to multiple Qase projects simultaneously, see the [Multi-Project Support Guide](MULTI_PROJECT.md).

---

## Test Stages as Steps

Each Tavern stage is automatically reported as a test step in Qase, providing detailed execution visibility.

### Basic Stages

```yaml
---
test_name: QaseID=1 Complete order flow

stages:
  - name: Add item to cart          # Reported as Step 1
    request:
      url: https://api.example.com/cart
      method: POST
      json:
        product_id: 123
        quantity: 1
    response:
      status_code: 201
      save:
        json:
          cart_id: id

  - name: Get cart contents         # Reported as Step 2
    request:
      url: https://api.example.com/cart/{cart_id}
      method: GET
    response:
      status_code: 200
      json:
        items:
          - product_id: 123
            quantity: 1

  - name: Checkout                  # Reported as Step 3
    request:
      url: https://api.example.com/checkout
      method: POST
      json:
        cart_id: "{cart_id}"
    response:
      status_code: 200
```

### Step Status

Each step's status is determined by its response validation:

| Stage Result | Step Status |
|--------------|-------------|
| All assertions pass | Passed |
| Assertion fails | Failed |
| Request error | Invalid |

---

## Test Result Statuses

| Tavern Result | Qase Status |
|---------------|-------------|
| All stages pass | `passed` |
| Stage assertion fails | `failed` |
| Stage request error | `invalid` |
| Test skipped | `skipped` |

---

## Multi-Project Support

Send test results to multiple Qase projects using `QaseProjectID.CODE=IDS` in the test name:

```yaml
---
test_name: QaseProjectID.PROJ1=1,2 QaseProjectID.PROJ2=10 Shared API test

stages:
  - name: Call shared endpoint
    request:
      url: https://api.example.com/shared
      method: GET
    response:
      status_code: 200
```

For detailed configuration, examples, and troubleshooting, see the [Multi-Project Support Guide](MULTI_PROJECT.md).

---

## Running Tests

### Basic Execution

```sh
pytest
```

### With CLI Options

```sh
pytest \
    --qase-mode=testops \
    --qase-testops-project=PROJ \
    --qase-testops-api-token=your_token
```

### With Environment Variables

```sh
export QASE_MODE=testops
export QASE_TESTOPS_PROJECT=PROJ
export QASE_TESTOPS_API_TOKEN=your_token
pytest
```

### Run Specific Test File

```sh
pytest test_users.tavern.yaml
```

### Run Specific Test

```sh
pytest test_users.tavern.yaml::test_get_user
```

### With Verbose Output

```sh
pytest -v --tb=short
```

---

## Complete Examples

### User CRUD Operations

```yaml
# test_users.tavern.yaml

---
test_name: QaseID=1 Create new user

stages:
  - name: Create user
    request:
      url: https://api.example.com/users
      method: POST
      json:
        name: "Test User"
        email: "test@example.com"
        role: "user"
    response:
      status_code: 201
      json:
        id: !anyint
        name: "Test User"
        email: "test@example.com"
      save:
        json:
          user_id: id

---
test_name: QaseID=2 Get user by ID

stages:
  - name: Get user
    request:
      url: https://api.example.com/users/{user_id}
      method: GET
    response:
      status_code: 200
      json:
        id: !int "{user_id}"
        name: "Test User"
        email: "test@example.com"

---
test_name: QaseID=3 Update user

stages:
  - name: Update user name
    request:
      url: https://api.example.com/users/{user_id}
      method: PUT
      json:
        name: "Updated User"
    response:
      status_code: 200
      json:
        id: !int "{user_id}"
        name: "Updated User"

---
test_name: QaseID=4 Delete user

stages:
  - name: Delete user
    request:
      url: https://api.example.com/users/{user_id}
      method: DELETE
    response:
      status_code: 204
```

### Authentication Flow

```yaml
# test_auth.tavern.yaml

---
test_name: QaseID=10,11 Complete authentication flow

stages:
  - name: Register new user
    request:
      url: https://api.example.com/auth/register
      method: POST
      json:
        email: "newuser@example.com"
        password: "SecurePass123"
        name: "New User"
    response:
      status_code: 201
      json:
        message: "User registered successfully"
      save:
        json:
          user_id: user_id

  - name: Login with credentials
    request:
      url: https://api.example.com/auth/login
      method: POST
      json:
        email: "newuser@example.com"
        password: "SecurePass123"
    response:
      status_code: 200
      json:
        token: !anystr
        user:
          id: !int "{user_id}"
          email: "newuser@example.com"
      save:
        json:
          auth_token: token

  - name: Access protected resource
    request:
      url: https://api.example.com/profile
      method: GET
      headers:
        Authorization: "Bearer {auth_token}"
    response:
      status_code: 200
      json:
        id: !int "{user_id}"
        name: "New User"

  - name: Logout
    request:
      url: https://api.example.com/auth/logout
      method: POST
      headers:
        Authorization: "Bearer {auth_token}"
    response:
      status_code: 200

  - name: Verify token is invalid
    request:
      url: https://api.example.com/profile
      method: GET
      headers:
        Authorization: "Bearer {auth_token}"
    response:
      status_code: 401
```

### Error Handling Tests

```yaml
# test_errors.tavern.yaml

---
test_name: QaseID=20 Invalid request returns 400

stages:
  - name: Send invalid request
    request:
      url: https://api.example.com/users
      method: POST
      json:
        name: ""  # Empty name should fail
    response:
      status_code: 400
      json:
        error: "Validation failed"
        details:
          - field: "name"
            message: "Name is required"

---
test_name: QaseID=21 Not found returns 404

stages:
  - name: Request non-existent resource
    request:
      url: https://api.example.com/users/999999
      method: GET
    response:
      status_code: 404
      json:
        error: "User not found"

---
test_name: QaseID=22 Unauthorized returns 401

stages:
  - name: Access without token
    request:
      url: https://api.example.com/profile
      method: GET
    response:
      status_code: 401
      json:
        error: "Authentication required"
```

### Example Project Structure

```
my-project/
├── qase.config.json
├── conftest.py
├── tests/
│   ├── test_users.tavern.yaml
│   ├── test_auth.tavern.yaml
│   ├── test_products.tavern.yaml
│   └── common.yaml           # Shared variables
└── requirements.txt
```

### Common Variables File

```yaml
# common.yaml

name: Common test variables

variables:
  base_url: "https://api.example.com"
  test_user: "testuser@example.com"
  test_password: "TestPass123"
```

---

## Troubleshooting

### Tests Not Appearing in Qase

1. Verify `mode` is set to `testops`
2. Check API token has write permissions
3. Verify project code is correct
4. Enable debug logging: `"debug": true`

### QaseID Not Recognized

1. Ensure format is exactly `QaseID=123` (case-sensitive)
2. No spaces around `=`
3. Multiple IDs use commas without spaces: `QaseID=1,2,3`

### Steps Not Showing

1. Verify stages have `name` field
2. Check stage syntax is valid YAML
3. Enable verbose output to see stage execution

### Response Validation Issues

1. Use `!anystr` and `!anyint` for dynamic values
2. Save values with `save.json` for use in later stages
3. Check response structure matches expected format

---

## See Also

- [Configuration Reference](../../qase-python-commons/README.md)
- [Multi-Project Support](MULTI_PROJECT.md)
- [Tavern Documentation](https://tavern.readthedocs.io/)
