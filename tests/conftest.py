import pytest

from qaseio.pytest.plugin import QasePytestPlugin

pytest_plugins = ["pytester"]


@pytest.fixture
def qs_plugin():
    def wrapper():
        return QasePytestPlugin("apitoken", "PRJCODE", 123)

    return wrapper
