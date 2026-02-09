"""
Attachment examples demonstrating Qase Pytest Reporter attachment functionality.

Attachments allow you to include files, screenshots, logs, and other data
with your test results in Qase TestOps for better debugging and documentation.
"""
import json
import os
import tempfile

from qase.pytest import qase


# ============================================================================
# Basic file attachments
# ============================================================================

def test_attach_single_file():
    """Attach a single file from the filesystem."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    attachments_dir = os.path.join(current_dir, "..", "attachments")

    # Attach a text file
    qase.attach(os.path.join(attachments_dir, "file.txt"))

    assert True, "File attached successfully"


def test_attach_multiple_files():
    """Attach multiple files at once."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    attachments_dir = os.path.join(current_dir, "..", "attachments")

    # Attach multiple files in a single call
    qase.attach(
        os.path.join(attachments_dir, "file.txt"),
        os.path.join(attachments_dir, "image.png")
    )

    assert True, "Multiple files attached successfully"


def test_attach_file_with_mime_type():
    """Attach a file with explicit MIME type specification."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    attachments_dir = os.path.join(current_dir, "..", "attachments")

    # Specify MIME type as tuple (filepath, mime_type)
    qase.attach((os.path.join(attachments_dir, "file.txt"), "text/plain"))

    assert True, "File with MIME type attached successfully"


# ============================================================================
# Byte data attachments
# ============================================================================

def test_attach_text_content():
    """Attach text content directly as bytes."""
    log_content = """
    [2024-01-15 10:30:00] INFO: Test started
    [2024-01-15 10:30:01] DEBUG: Connecting to database
    [2024-01-15 10:30:02] INFO: Database connection established
    [2024-01-15 10:30:03] DEBUG: Executing query
    [2024-01-15 10:30:04] INFO: Test completed successfully
    """

    # Attach bytes with MIME type and filename: (bytes, mime_type, filename)
    qase.attach((log_content.encode("utf-8"), "text/plain", "test_execution.log"))

    assert True, "Text content attached as bytes"


def test_attach_json_data():
    """Attach JSON data from a dictionary."""
    api_response = {
        "status": "success",
        "code": 200,
        "data": {
            "user_id": 12345,
            "username": "testuser",
            "email": "test@example.com",
            "roles": ["user", "admin"]
        },
        "metadata": {
            "request_id": "req-abc-123",
            "timestamp": "2024-01-15T10:30:00Z"
        }
    }

    json_bytes = json.dumps(api_response, indent=2).encode("utf-8")
    qase.attach((json_bytes, "application/json", "api_response.json"))

    assert api_response["status"] == "success"


def test_attach_csv_report():
    """Attach CSV data as a report."""
    csv_content = """id,name,status,duration_ms
1,test_login,passed,120
2,test_logout,passed,85
3,test_profile,failed,250
4,test_settings,passed,95
5,test_dashboard,skipped,0
"""

    qase.attach((csv_content.encode("utf-8"), "text/csv", "test_report.csv"))

    assert True, "CSV report attached"


def test_attach_html_report():
    """Attach HTML content as a report."""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head><title>Test Report</title></head>
    <body>
        <h1>Test Execution Summary</h1>
        <table border="1">
            <tr><th>Test</th><th>Status</th><th>Duration</th></tr>
            <tr><td>Login Test</td><td style="color:green">PASSED</td><td>1.2s</td></tr>
            <tr><td>Checkout Test</td><td style="color:green">PASSED</td><td>3.5s</td></tr>
            <tr><td>Search Test</td><td style="color:red">FAILED</td><td>2.1s</td></tr>
        </table>
        <p>Total: 3 tests, 2 passed, 1 failed</p>
    </body>
    </html>
    """

    qase.attach((html_content.encode("utf-8"), "text/html", "summary_report.html"))

    assert True, "HTML report attached"


# ============================================================================
# Dynamic content attachments
# ============================================================================

def test_attach_error_screenshot_simulation():
    """Simulate attaching a screenshot when an error occurs."""
    try:
        # Simulated operation that might fail
        result = perform_risky_operation()
        assert result["success"], "Operation should succeed"

    except AssertionError:
        # In real scenario, capture screenshot here
        error_info = """
        ERROR DETAILS
        =============
        Operation: perform_risky_operation
        Error: AssertionError - Operation should succeed
        Timestamp: 2024-01-15T10:30:00Z

        Stack trace:
        File "test_attachments.py", line XX, in test_attach_error_screenshot_simulation
            assert result["success"], "Operation should succeed"
        """
        qase.attach((error_info.encode("utf-8"), "text/plain", "error_details.txt"))
        raise


def perform_risky_operation():
    """Helper function that simulates an operation."""
    return {"success": True, "data": "result"}


def test_attach_performance_metrics():
    """Attach performance metrics collected during test."""
    # Simulate collecting performance data
    metrics = {
        "test_name": "API Response Time Test",
        "iterations": 100,
        "results": {
            "min_ms": 45,
            "max_ms": 320,
            "avg_ms": 85,
            "p50_ms": 78,
            "p90_ms": 150,
            "p99_ms": 280
        },
        "passed_threshold": True,
        "threshold_ms": 200
    }

    # Attach as JSON for structured data
    qase.attach((
        json.dumps(metrics, indent=2).encode("utf-8"),
        "application/json",
        "performance_metrics.json"
    ))

    assert metrics["passed_threshold"], "Performance should be within threshold"


# ============================================================================
# Attachments within steps
# ============================================================================

@qase.step("Execute API request and capture response")
def execute_api_request(endpoint: str) -> dict:
    """Step that executes API request and attaches the response."""
    # Simulated API request
    response = {
        "endpoint": endpoint,
        "method": "GET",
        "status_code": 200,
        "headers": {
            "content-type": "application/json",
            "x-request-id": "req-123"
        },
        "body": {
            "data": [{"id": 1}, {"id": 2}]
        }
    }

    # Attach request/response details
    qase.attach((
        json.dumps(response, indent=2).encode("utf-8"),
        "application/json",
        f"api_response_{endpoint.replace('/', '_')}.json"
    ))

    return response


@qase.step("Validate response data")
def validate_response(response: dict, expected_status: int) -> bool:
    """Step that validates response and attaches validation report."""
    validation_results = {
        "checks": [
            {"name": "status_code", "expected": expected_status, "actual": response["status_code"], "passed": response["status_code"] == expected_status},
            {"name": "has_body", "expected": True, "actual": "body" in response, "passed": "body" in response},
            {"name": "has_data", "expected": True, "actual": "data" in response.get("body", {}), "passed": "data" in response.get("body", {})}
        ],
        "all_passed": True
    }

    validation_results["all_passed"] = all(c["passed"] for c in validation_results["checks"])

    qase.attach((
        json.dumps(validation_results, indent=2).encode("utf-8"),
        "application/json",
        "validation_report.json"
    ))

    return validation_results["all_passed"]


def test_api_flow_with_step_attachments():
    """Test demonstrating attachments within steps."""
    # Step 1: Make API request (attaches response)
    response = execute_api_request("/api/users")
    assert response["status_code"] == 200

    # Step 2: Validate response (attaches validation report)
    is_valid = validate_response(response, 200)
    assert is_valid, "Response validation should pass"


# ============================================================================
# Temporary file attachments
# ============================================================================

def test_attach_generated_file():
    """Generate a file during test and attach it."""
    # Create a temporary file with test results
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write("Generated Test Results\n")
        f.write("=" * 40 + "\n")
        f.write("Test: test_attach_generated_file\n")
        f.write("Status: PASSED\n")
        f.write("Duration: 0.5s\n")
        temp_path = f.name

    try:
        # Attach the generated file
        qase.attach((temp_path, "text/plain"))
        assert True, "Generated file attached"
    finally:
        # Clean up
        os.unlink(temp_path)


# ============================================================================
# Practical scenarios
# ============================================================================

@qase.id(50)
@qase.title("Database query execution with result attachment")
@qase.severity("normal")
def test_database_query_with_attachment():
    """Practical example: attach database query results."""
    # Simulated database query
    query = "SELECT id, name, email FROM users WHERE status = 'active' LIMIT 10"
    results = [
        {"id": 1, "name": "Alice", "email": "alice@example.com"},
        {"id": 2, "name": "Bob", "email": "bob@example.com"},
        {"id": 3, "name": "Charlie", "email": "charlie@example.com"},
    ]

    # Attach query for reference
    qase.attach((query.encode("utf-8"), "text/plain", "executed_query.sql"))

    # Attach results as JSON
    qase.attach((
        json.dumps(results, indent=2).encode("utf-8"),
        "application/json",
        "query_results.json"
    ))

    assert len(results) > 0, "Query should return results"


@qase.id(51)
@qase.title("Configuration validation with config attachment")
def test_config_validation_with_attachment():
    """Practical example: validate and attach configuration."""
    config = {
        "app": {
            "name": "TestApp",
            "version": "1.0.0",
            "environment": "staging"
        },
        "database": {
            "host": "db.example.com",
            "port": 5432,
            "pool_size": 10
        },
        "features": {
            "dark_mode": True,
            "beta_features": False
        }
    }

    # Attach the configuration being tested
    qase.attach((
        json.dumps(config, indent=2).encode("utf-8"),
        "application/json",
        "test_config.json"
    ))

    # Validate configuration
    assert config["app"]["name"], "App name must be set"
    assert config["database"]["port"] > 0, "Database port must be positive"
    assert "environment" in config["app"], "Environment must be specified"
