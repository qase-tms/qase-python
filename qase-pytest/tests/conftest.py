import re

import pytest

import requests_mock

from qaseio.pytest.plugin import QasePytestPlugin, QasePytestPluginSingleton

pytest_plugins = ["pytester"]


@pytest.fixture
def mock() -> requests_mock.Mocker:
    QasePytestPluginSingleton._instance = None
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
        mock.post(
            f"/v1/run/{project}",
            json={"status": True, "result": {"id": 3}},
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
def results_mocks(mock):
    def wrapper(regex=r".*/result/[a-zA-Z]+/\d+", **kwargs):
        mock.post(
            re.compile(regex),
            json={"status": True, "result": {"hash": "1a2b3d"}},
            **kwargs,
        )
        mock.patch(
            re.compile(regex + r"/.*"),
            json={"status": True, "result": {"hash": "1a2b3d"}},
            **kwargs,
        )

    return wrapper


@pytest.fixture
def attachment_mocks(mock):
    def wrapper(regex=r".*/attachment/[a-zA-Z]+", **kwargs):
        mock.post(
            re.compile(regex),
            json={
                "status": True,
                "result": [
                    {
                        "filename": "qaseio_pytest.py",
                        "url": "https://storage.cdn.example/filename.ext",
                        "extension": "py",
                        "hash": "d81bb2beb147c2eceddbf3e10f98e6216cc757e3",
                        "mime": "text\\/x-python",
                        "team": "c66dc393c83fe149449e5de3e64545279e1442ed",
                    }
                ],
            },
            **kwargs,
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
