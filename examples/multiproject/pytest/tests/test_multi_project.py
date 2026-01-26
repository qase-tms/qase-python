"""
Simple tests for multi-project support.

These tests demonstrate how to send test results to multiple projects
with different test case IDs using the @qase.project_id decorator.
"""
import pytest
from qase.pytest import qase


@qase.project_id("DEVX", 1)
def test_single_project_single_id():
    """Test with single project and single ID."""
    assert True


@qase.project_id("DEVX", [2, 3])
def test_single_project_multiple_ids():
    """Test with single project and multiple IDs."""
    assert 1 + 1 == 2


@qase.project_id("DEVX", 4)
@qase.project_id("DEMO", 10)
def test_multiple_projects_single_id():
    """Test with multiple projects, each with single ID."""
    assert "hello" == "hello"


@qase.project_id("DEVX", [5, 6])
@qase.project_id("DEMO", [11, 12])
def test_multiple_projects_multiple_ids():
    """Test with multiple projects, each with multiple IDs."""
    result = 2 * 3
    assert result == 6


@qase.project_id("DEVX", 7)
def test_failed_test_devx():
    """This test will fail and should be reported to DEVX project."""
    assert False, "This test intentionally fails"


@qase.project_id("DEMO", 13)
def test_passed_test_demo():
    """This test will pass and should be reported to DEMO project."""
    assert True


@pytest.mark.parametrize("value", [1, 2, 3])
@qase.project_id("DEVX", 8)
def test_parametrized_devx(value):
    """Parametrized test for DEVX project."""
    assert value > 0


@pytest.mark.parametrize("value", [10, 20])
@qase.project_id("DEMO", 14)
def test_parametrized_demo(value):
    """Parametrized test for DEMO project."""
    assert value % 10 == 0


def test_without_id():
    """Test without any ID - should be sent to first project (DEVX) from config."""
    assert True
