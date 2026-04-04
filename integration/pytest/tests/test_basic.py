"""Basic pass/fail/skip tests with QaseIds for unique signatures."""
import pytest
from qase.pytest import qase


@qase.id(101)
@qase.title("Simple passing test")
def test_pass():
    assert True


@qase.id(102)
@qase.title("Simple failing test")
def test_fail():
    assert False, "Intentional failure"


@qase.id(103)
@qase.title("Skipped test")
@pytest.mark.skip(reason="Skipped for integration testing")
def test_skip():
    assert True
