# Qase Integration in Tavern

This guide demonstrates how to integrate Qase with Tavern, providing instructions on how to add Qase IDs and other metadata to your API test cases.

> **Configuration:** For complete configuration reference including all available options, environment variables, and examples, see the [qase-python-commons README](../../qase-python-commons/README.md).

---

## Adding QaseID to a Test

To associate a QaseID with a test in Tavern, include `QaseID={ID}` in the test name.

```yaml
---
test_name: QaseID=1 Get user by ID

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
        email: "john@example.com"
```

### Multiple Qase IDs

You can associate multiple Qase IDs with a single test by separating them with commas:

```yaml
---
test_name: QaseID=1,2,3 Get user by ID

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
        email: "john@example.com"
```

### Multi-Project Support

Qase Tavern Reporter supports sending test results to multiple Qase projects simultaneously with different test case IDs for each project.

For detailed information, configuration, examples, and troubleshooting, see the [Multi-Project Support Guide](MULTI_PROJECT.md).

---

## Examples

### Complete Test File Example

```yaml
---
test_name: QaseID=1 Get user by ID success

stages:
  - name: Get user
    request:
      url: https://jsonplaceholder.typicode.com/posts/1
      method: GET
    response:
      status_code: 200
      json:
        id: 1
        userId: 1
        title: "sunt aut facere repellat provident occaecati excepturi optio reprehenderit"
        body: "quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto"

---
test_name: QaseID=2 Get user by ID failed

stages:
  - name: Get user
    request:
      url: https://jsonplaceholder.typicode.com/posts/1
      method: GET
    response:
      status_code: 300  # This will cause the test to fail
      json:
        id: 1
        userId: 1
        title: "sunt aut facere repellat provident occaecati excepturi optio reprehenderit"
        body: "quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto"

---
test_name: QaseID=3,4 User authentication flow

stages:
  - name: Login user
    request:
      url: https://api.example.com/auth/login
      method: POST
      json:
        username: "testuser"
        password: "testpass"
    response:
      status_code: 200
      json:
        token: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

  - name: Get user profile
    request:
      url: https://api.example.com/user/profile
      method: GET
      headers:
        Authorization: "Bearer {token}"
    response:
      status_code: 200
      json:
        id: 1
        name: "Test User"
        email: "test@example.com"

  - name: Update user profile
    request:
      url: https://api.example.com/user/profile
      method: PUT
      headers:
        Authorization: "Bearer {token}"
      json:
        name: "Updated User"
        email: "updated@example.com"
    response:
      status_code: 200
      json:
        id: 1
        name: "Updated User"
        email: "updated@example.com"
```

### Running Tests

```bash
# Basic run
pytest --qase-mode=testops --qase-testops-project=MYPROJECT --qase-testops-api-token=YOUR_TOKEN test_file.tavern.yaml

# With environment and plan
pytest --qase-mode=testops --qase-testops-project=MYPROJECT --qase-testops-api-token=YOUR_TOKEN --qase-environment=staging --qase-testops-plan-id=123 test_file.tavern.yaml

# With execution plan
pytest --qase-mode=testops --qase-testops-project=MYPROJECT --qase-testops-api-token=YOUR_TOKEN --qase-execution-plan-path=plan.json test_file.tavern.yaml

# With profilers and logs
pytest --qase-mode=testops --qase-testops-project=MYPROJECT --qase-testops-api-token=YOUR_TOKEN --qase-profilers=network,db --qase-pytest-capture-logs=true test_file.tavern.yaml
```
