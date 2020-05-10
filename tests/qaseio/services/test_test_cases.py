import pytest

import requests_mock
from apitist.constructor import converter
from tests.data import _list, _status_true, _test_case

from qaseio.client.models import (
    Severity,
    TestCaseFilters,
    TestCaseInfo,
    TestCaseList,
)


@pytest.mark.parametrize(
    "params, query",
    [
        ((10, 30), "?limit=10&offset=30"),
        ((None, 30), "?offset=30"),
        ((10, None), "?limit=10"),
        (
            (
                10,
                None,
                TestCaseFilters(
                    severity=[Severity.CRITICAL, Severity.BLOCKER]
                ),
            ),
            "?limit=10&filters%5Bseverity%5D=critical%2Cblocker",
        ),
    ],
)
def test_get_all_test_cases(client, params, query):
    response = _status_true(_list(_test_case()))
    with requests_mock.Mocker() as m:
        m.get(client._path("case/CODE"), json=response)
        data = client.cases.get_all("CODE", *params)
        assert data == converter.structure(
            response.get("result"), TestCaseList
        )
        res = client.cases._last_res
        assert res.url == client._path("case/CODE" + query)


def test_get_specific_test_case(client):
    response = _status_true(_test_case())
    with requests_mock.Mocker() as m:
        m.get(client._path("case/CODE/123"), json=response)
        data = client.cases.get("CODE", 123)
        assert data == converter.structure(
            response.get("result"), TestCaseInfo
        )
        res = client.cases._last_res
        assert res.url == client._path("case/CODE/123")


def test_test_case_exists(client):
    response = _status_true(_test_case())
    with requests_mock.Mocker() as m:
        m.get(
            client._path("case/CODE/123"),
            [
                {"status_code": 200, "json": response},
                {"status_code": 404, "json": {}},
            ],
        )
        assert client.cases.exists("CODE", 123)
        assert not client.cases.exists("CODE", 123)


def test_delete_test_case(client):
    with requests_mock.Mocker() as m:
        m.delete(client._path("case/CODE/123"), json={"status": True})
        data = client.cases.delete("CODE", 123)
        assert data is None
        res = client.cases._last_res
        assert res.url == client._path("case/CODE/123")
