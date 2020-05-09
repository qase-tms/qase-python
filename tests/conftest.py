import re

import pytest

import requests_mock

from qaseio.pytest.plugin import QasePytestPlugin

pytest_plugins = ["pytester"]


@pytest.fixture
def mock() -> requests_mock.Mocker:
    with requests_mock.Mocker() as m:
        yield m


@pytest.fixture
def default_mocks(mock):
    def wrapper(project="PRJ", run_id=3):
        mock.get(f"/v1/project/{project}", json={"status": True, "result": {}})
        mock.get(
            f"/v1/run/{project}/{run_id}",
            json={
                "status": True,
                "result": {"cases": [i for i in range(1, 16) if i not in [3]]},
            },
        )

    return wrapper


@pytest.fixture
def cases_mocks(mock):
    def wrapper(regex=r".*/case/[a-zA-Z]+/\d+", **kwargs):
        mock.get(
            re.compile(regex), json={"status": True, "result": {}}, **kwargs
        )

    return wrapper


@pytest.fixture
def qs_plugin(default_mocks):
    def wrapper(**kwargs):
        default_mocks("PRJCODE", 123)
        kwargs["api_token"] = kwargs.get("api_token", "apitoken")
        kwargs["project"] = kwargs.get("project", "PRJCODE")
        kwargs["testrun"] = kwargs.get("testrun", 123)
        return QasePytestPlugin(**kwargs)

    return wrapper
