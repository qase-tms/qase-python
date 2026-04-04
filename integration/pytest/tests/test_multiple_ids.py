"""Tests demonstrating multiple QaseIds on a single test."""
from qase.pytest import qase


@qase.id([701, 702])
@qase.title("Test linked to multiple Qase test cases")
def test_multiple_ids():
    assert True
