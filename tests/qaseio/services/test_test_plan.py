import json

import pytest

import requests_mock
from apitist.constructor import converter
from tests.data import _list, _status_true, _test_plan, _test_plan_full

from qaseio.client.models import (
    TestPlanCreate,
    TestPlanCreated,
    TestPlanInfo,
    TestPlanList,
    TestPlanUpdate,
)


@pytest.mark.parametrize(
    "params, query",
    [
        ((10, 30), "?limit=10&offset=30"),
        ((None, 30), "?offset=30"),
        ((10, None), "?limit=10"),
    ],
)
def test_get_all_test_plans(client, params, query):
    response = _status_true(_list(_test_plan()))
    with requests_mock.Mocker() as m:
        m.get(client._path("plan/CODE"), json=response)
        data = client.plans.get_all("CODE", *params)
        assert data == converter.structure(
            response.get("result"), TestPlanList
        )
        res = client.plans._last_res
        assert res.url == client._path("plan/CODE" + query)


def test_get_specific_test_plan(client):
    response = _status_true(_test_plan_full())
    with requests_mock.Mocker() as m:
        m.get(client._path("plan/CODE/123"), json=response)
        data = client.plans.get("CODE", 123)
        assert data == converter.structure(
            response.get("result"), TestPlanInfo
        )
        res = client.plans._last_res
        assert res.url == client._path("plan/CODE/123")


def test_test_plan_exists(client):
    response = _status_true(_test_plan_full())
    with requests_mock.Mocker() as m:
        m.get(
            client._path("plan/CODE/123"),
            [
                {"status_code": 200, "json": response},
                {"status_code": 404, "json": {}},
            ],
        )
        assert client.plans.exists("CODE", 123)
        assert not client.plans.exists("CODE", 123)


def test_create_new_test_plan(client):
    response = _status_true({"id": 123})
    with requests_mock.Mocker() as m:
        m.post(client._path("plan/CODE"), json=response)
        create_data = TestPlanCreate("new test plan", [1, 2, 3])
        data = client.plans.create("CODE", create_data)
        assert data == converter.structure(
            response.get("result"), TestPlanCreated
        )
        res = client.plans._last_res
        assert json.loads(res.request.body) == converter.unstructure(
            create_data
        )


def test_update_test_plan(client):
    response = _status_true({"id": 123})
    with requests_mock.Mocker() as m:
        m.patch(client._path("plan/CODE/123"), json=response)
        update_data = TestPlanUpdate("new test plan", [1, 2, 3])
        data = client.plans.update("CODE", 123, update_data)
        assert data == converter.structure(
            response.get("result"), TestPlanCreated
        )
        res = client.plans._last_res
        assert res.url == client._path("plan/CODE/123")
        assert json.loads(res.request.body) == converter.unstructure(
            update_data
        )


def test_delete_test_plan(client):
    with requests_mock.Mocker() as m:
        m.delete(client._path("plan/CODE/123"), json={"status": True})
        data = client.plans.delete("CODE", 123)
        assert data is None
        res = client.plans._last_res
        assert res.url == client._path("plan/CODE/123")
