import pytest

import requests_mock

from qaseio.pytest.plugin import QasePytestPlugin

pytest_plugins = ["pytester"]


@pytest.fixture
def mock() -> requests_mock.Mocker:
    with requests_mock.Mocker() as m:
        yield m


@pytest.fixture
def qs_plugin(mock):
    def wrapper():
        mock.get("/v1/project/PRJCODE", json={"status": True, "result": {}})
        mock.get(
            "/v1/run/PRJCODE/123",
            json={"status": True, "result": {"cases": [1, 2, 3]}},
        )
        return QasePytestPlugin("apitoken", "PRJCODE", 123)

    return wrapper
