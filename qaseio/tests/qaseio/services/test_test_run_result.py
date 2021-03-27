import json

import pytest

import requests_mock
from apitist.constructor import converter
from tests.data import _list, _status_true, _test_run_result

from qaseio.client.models import (
    TestRunResultCreate,
    TestRunResultCreated,
    TestRunResultFilters,
    TestRunResultInfo,
    TestRunResultList,
    TestRunResultStatus,
    TestRunResultUpdate,
)


@pytest.mark.parametrize(
    "params, query",
    [
        (
            (
                10,
                30,
                TestRunResultFilters(status=[TestRunResultStatus.FAILED]),
            ),
            "?limit=10&offset=30&filters%5Bstatus%5D=failed",
        ),
        ((None, 30, None), "?offset=30"),
        ((10, None, None), "?limit=10"),
        (
            (
                None,
                None,
                TestRunResultFilters(status=[TestRunResultStatus.FAILED]),
            ),
            "?filters%5Bstatus%5D=failed",
        ),
    ],
)
def test_get_all_test_run_results(client, params, query):
    response = _status_true(_list(_test_run_result()))
    with requests_mock.Mocker() as m:
        m.get(client._path("result/CODE"), json=response)
        data = client.results.get_all("CODE", *params)
        assert data == converter.structure(
            response.get("result"), TestRunResultList
        )
        res = client.results._last_res
        assert res.url == client._path("result/CODE" + query)


def test_get_specific_test_run_result(client):
    response = _status_true(_test_run_result())
    with requests_mock.Mocker() as m:
        m.get(client._path("result/CODE/6efce6e4"), json=response)
        data = client.results.get("CODE", "6efce6e4")
        assert data == converter.structure(
            response.get("result"), TestRunResultInfo
        )
        res = client.results._last_res
        assert res.url == client._path("result/CODE/6efce6e4")


def test_create_new_test_run_result(client):
    response = _status_true({"hash": "6efce6e4"})
    with requests_mock.Mocker() as m:
        m.post(client._path("result/CODE/123"), json=response)
        create_data = TestRunResultCreate(123, TestRunResultStatus.BLOCKED)
        data = client.results.create("CODE", 123, create_data)
        assert data == converter.structure(
            response.get("result"), TestRunResultCreated
        )
        res = client.results._last_res
        assert json.loads(res.request.body) == converter.unstructure(
            create_data
        )


def test_update_test_run_result(client):
    response = _status_true({"hash": "6efce6e4"})
    with requests_mock.Mocker() as m:
        m.patch(client._path("result/CODE/123/6efce6e4"), json=response)
        update_data = TestRunResultUpdate(TestRunResultStatus.BLOCKED)
        data = client.results.update("CODE", 123, "6efce6e4", update_data)
        assert data == converter.structure(
            response.get("result"), TestRunResultCreated
        )
        res = client.results._last_res
        assert res.url == client._path("result/CODE/123/6efce6e4")
        assert json.loads(res.request.body) == converter.unstructure(
            update_data
        )


def test_delete_test_run_result(client):
    with requests_mock.Mocker() as m:
        m.delete(
            client._path("result/CODE/123/6efce6e4"), json={"status": True}
        )
        data = client.results.delete("CODE", 123, "6efce6e4")
        assert data is None
        res = client.results._last_res
        assert res.url == client._path("result/CODE/123/6efce6e4")
