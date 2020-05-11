import json

import pytest

import requests_mock
from apitist.constructor import converter
from tests.data import _list, _shared_step, _status_true

from qaseio.client.models import (
    SharedStepCreate,
    SharedStepCreated,
    SharedStepFilters,
    SharedStepInfo,
    SharedStepList,
    SharedStepUpdate,
)


@pytest.mark.parametrize(
    "params, query",
    [
        ((10, 30), "?limit=10&offset=30"),
        ((None, 30), "?offset=30"),
        ((10, None), "?limit=10"),
        (
            (10, None, SharedStepFilters(search="123"),),
            "?limit=10&filters%5Bsearch%5D=123",
        ),
    ],
)
def test_get_all_shared_steps(client, params, query):
    response = _status_true(_list(_shared_step()))
    with requests_mock.Mocker() as m:
        m.get(client._path("shared_step/CODE"), json=response)
        data = client.shared_steps.get_all("CODE", *params)
        assert data == converter.structure(
            response.get("result"), SharedStepList
        )
        res = client.shared_steps._last_res
        assert res.url == client._path("shared_step/CODE" + query)


def test_get_specific_shared_step(client):
    response = _status_true(_shared_step())
    with requests_mock.Mocker() as m:
        m.get(client._path("shared_step/CODE/hash"), json=response)
        data = client.shared_steps.get("CODE", "hash")
        assert data == converter.structure(
            response.get("result"), SharedStepInfo
        )
        res = client.shared_steps._last_res
        assert res.url == client._path("shared_step/CODE/hash")


def test_shared_step_exists(client):
    response = _status_true(_shared_step())
    with requests_mock.Mocker() as m:
        m.get(
            client._path("shared_step/CODE/hash"),
            [
                {"status_code": 200, "json": response},
                {"status_code": 404, "json": {}},
            ],
        )
        assert client.shared_steps.exists("CODE", "hash")
        assert not client.shared_steps.exists("CODE", "hash")


def test_create_new_shared_step(client):
    response = _status_true({"hash": "hash"})
    with requests_mock.Mocker() as m:
        m.post(client._path("shared_step/CODE"), json=response)
        create_data = SharedStepCreate("new test", "action")
        data = client.shared_steps.create("CODE", create_data)
        assert data == converter.structure(
            response.get("result"), SharedStepCreated
        )
        res = client.shared_steps._last_res
        assert json.loads(res.request.body) == converter.unstructure(
            create_data
        )


def test_update_shared_step(client):
    response = _status_true({"hash": "hash"})
    with requests_mock.Mocker() as m:
        m.patch(client._path("shared_step/CODE/hash"), json=response)
        update_data = SharedStepUpdate("new test")
        data = client.shared_steps.update("CODE", "hash", update_data)
        assert data == converter.structure(
            response.get("result"), SharedStepCreated
        )
        res = client.shared_steps._last_res
        assert res.url == client._path("shared_step/CODE/hash")
        assert json.loads(res.request.body) == converter.unstructure(
            update_data
        )


def test_delete_shared_step(client):
    with requests_mock.Mocker() as m:
        m.delete(client._path("shared_step/CODE/hash"), json={"status": True})
        data = client.shared_steps.delete("CODE", "hash")
        assert data is None
        res = client.shared_steps._last_res
        assert res.url == client._path("shared_step/CODE/hash")
