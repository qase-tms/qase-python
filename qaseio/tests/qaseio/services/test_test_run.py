import json

import pytest

import requests_mock
from apitist.constructor import converter
from tests.data import _list, _status_true, _test_run

from qaseio.client.models import (
    TestRunCreate,
    TestRunCreated,
    TestRunFilters,
    TestRunInclude,
    TestRunInfo,
    TestRunList,
    TestRunStatus,
)


@pytest.mark.parametrize(
    "params, query",
    [
        ((10, 30, TestRunInclude.CASES), "?limit=10&offset=30&include=cases"),
        ((None, 30, None), "?offset=30"),
        ((10, None, None), "?limit=10"),
        ((None, None, TestRunInclude.CASES), "?include=cases"),
        (
            (None, None, None, TestRunFilters(status=[TestRunStatus.ABORT])),
            "?filters%5Bstatus%5D=abort",
        ),
    ],
)
def test_get_all_test_runs(client, params, query):
    response = _status_true(_list(_test_run()))
    with requests_mock.Mocker() as m:
        m.get(client._path("run/CODE"), json=response)
        data = client.runs.get_all("CODE", *params)
        assert data == converter.structure(response.get("result"), TestRunList)
        res = client.runs._last_res
        assert res.url == client._path("run/CODE" + query)


def test_get_specific_test_run(client):
    response = _status_true(_test_run())
    with requests_mock.Mocker() as m:
        m.get(client._path("run/CODE/123"), json=response)
        data = client.runs.get("CODE", 123)
        assert data == converter.structure(response.get("result"), TestRunInfo)
        res = client.runs._last_res
        assert res.url == client._path("run/CODE/123")


def test_test_run_exists(client):
    response = _status_true(_test_run())
    with requests_mock.Mocker() as m:
        m.get(
            client._path("run/CODE/123"),
            [
                {"status_code": 200, "json": response},
                {"status_code": 404, "json": {}},
            ],
        )
        assert client.runs.exists("CODE", 123)
        assert not client.runs.exists("CODE", 123)


def test_create_new_test_run(client):
    response = _status_true({"id": 123})
    with requests_mock.Mocker() as m:
        m.post(client._path("run/CODE"), json=response)
        create_data = TestRunCreate("new test run", [1, 2, 3])
        data = client.runs.create("CODE", create_data)
        assert data == converter.structure(
            response.get("result"), TestRunCreated
        )
        res = client.runs._last_res
        assert json.loads(res.request.body) == converter.unstructure(
            create_data
        )


def test_delete_test_run(client):
    with requests_mock.Mocker() as m:
        m.delete(client._path("run/CODE/123"), json={"status": True})
        data = client.runs.delete("CODE", 123)
        assert data is None
        res = client.runs._last_res
        assert res.url == client._path("run/CODE/123")
