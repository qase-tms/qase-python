from _pytest.mark import MarkDecorator

from qase.pytest import qase

def test_pytest_mark():
    assert isinstance(qase.id(5), MarkDecorator)