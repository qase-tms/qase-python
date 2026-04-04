"""Tests demonstrating parametrized tests."""
import pytest
from qase.pytest import qase


@qase.id(401)
@qase.title("Parametrized test with single param")
@pytest.mark.parametrize("value", [1, 2, 3])
def test_single_param(value):
    assert value > 0


@qase.id(402)
@qase.title("Parametrized test with multiple params")
@pytest.mark.parametrize("a,b,expected", [
    (1, 2, 3),
    (4, 5, 9),
])
def test_multiple_params(a, b, expected):
    assert a + b == expected
