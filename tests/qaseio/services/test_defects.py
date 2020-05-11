import pytest

import requests_mock
from apitist.constructor import converter
from tests.data import _defect, _list, _status_true

from qaseio.client.models import (
    DefectFilters,
    DefectInfo,
    DefectList,
    DefectStatus,
    DefectUpdated,
)


@pytest.mark.parametrize(
    "params, query",
    [
        ((10, 30), "?limit=10&offset=30"),
        ((None, 30), "?offset=30"),
        ((10, None), "?limit=10"),
        (
            (10, None, DefectFilters(status=DefectStatus.OPEN),),
            "?limit=10&filters%5Bstatus%5D=open",
        ),
    ],
)
def test_get_all_defects(client, params, query):
    response = _status_true(_list(_defect()))
    with requests_mock.Mocker() as m:
        m.get(client._path("defect/CODE"), json=response)
        data = client.defects.get_all("CODE", *params)
        assert data == converter.structure(response.get("result"), DefectList)
        res = client.defects._last_res
        assert res.url == client._path("defect/CODE" + query)


def test_get_specific_defect(client):
    response = _status_true(_defect())
    with requests_mock.Mocker() as m:
        m.get(client._path("defect/CODE/123"), json=response)
        data = client.defects.get("CODE", 123)
        assert data == converter.structure(response.get("result"), DefectInfo)
        res = client.defects._last_res
        assert res.url == client._path("defect/CODE/123")


def test_defect_exists(client):
    response = _status_true(_defect())
    with requests_mock.Mocker() as m:
        m.get(
            client._path("defect/CODE/123"),
            [
                {"status_code": 200, "json": response},
                {"status_code": 404, "json": {}},
            ],
        )
        assert client.defects.exists("CODE", 123)
        assert not client.defects.exists("CODE", 123)


def test_resolve_defect(client):
    response = _status_true({"id": 123})
    with requests_mock.Mocker() as m:
        m.patch(client._path("defect/CODE/resolve/123"), json=response)
        data = client.defects.resolve("CODE", 123)
        assert data == converter.structure(
            response.get("result"), DefectUpdated
        )


def test_delete_defect(client):
    with requests_mock.Mocker() as m:
        m.delete(client._path("defect/CODE/123"), json={"status": True})
        data = client.defects.delete("CODE", 123)
        assert data is None
        res = client.defects._last_res
        assert res.url == client._path("defect/CODE/123")
