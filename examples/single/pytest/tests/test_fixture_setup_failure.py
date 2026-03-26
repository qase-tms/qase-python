"""
Examples demonstrating log capture for fixture setup failures.

These tests show how the Qase reporter handles logs when fixtures
fail during setup phase (pytest reports these as ERROR, not FAILED).
"""
import logging
import sys

import pytest


# ============================================================================
# Fixtures that fail during setup
# ============================================================================

@pytest.fixture
def broken_database_connection():
    """Fixture that simulates a database connection failure during setup."""
    logging.info("Attempting to connect to database...")
    logging.warning("Connection timeout approaching...")
    print("stdout: Connecting to db at localhost:5432...")
    print("stderr: Connection refused", file=sys.stderr)
    raise ConnectionError("Failed to connect to database at localhost:5432")


@pytest.fixture
def broken_api_client():
    """Fixture that simulates an API client initialization failure."""
    logging.info("Initializing API client...")
    logging.error("API token validation failed")
    print("stdout: Validating API token...")
    raise ValueError("Invalid API token: token has expired")


@pytest.fixture
def working_fixture():
    """Fixture that works fine - setup logs should NOT be duplicated."""
    logging.info("Setting up working fixture")
    print("stdout: Working fixture ready")
    return {"status": "ready"}


# ============================================================================
# Tests using broken fixtures - these will ERROR during setup
# ============================================================================

def test_query_users(broken_database_connection):
    """This test will ERROR because the database fixture fails.

    The reporter should capture fixture setup logs (log.txt, stdout.txt,
    stderr.txt) and attach them to the Qase result.
    """
    broken_database_connection.execute("SELECT * FROM users")


def test_fetch_api_data(broken_api_client):
    """This test will ERROR because the API client fixture fails.

    Setup-phase logs should be captured and attached.
    """
    broken_api_client.get("/api/data")


# ============================================================================
# Tests using working fixtures - no log duplication expected
# ============================================================================

def test_with_working_fixture(working_fixture):
    """This test passes normally.

    Setup-phase logs should NOT be attached (only call-phase logs),
    to avoid duplicate attachments.
    """
    assert working_fixture["status"] == "ready"
    logging.info("Test executed successfully")
    print("stdout: Test running...")
