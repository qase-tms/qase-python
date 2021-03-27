import pytest

import requests_mock
from apitist.constructor import converter
from tests.data import _custom_field, _list, _status_true

from qaseio.client.models import CustomFieldInfo, CustomFieldList


@pytest.mark.parametrize(
    "params, query",
    [
        ((10, 30), "?limit=10&offset=30"),
        ((None, 30), "?offset=30"),
        ((10, None), "?limit=10"),
    ],
)
def test_get_all_custom_fields(client, params, query):
    response = _status_true(_list(_custom_field()))
    with requests_mock.Mocker() as m:
        m.get(client._path("custom_field/CODE"), json=response)
        data = client.custom_fields.get_all("CODE", *params)
        assert data == converter.structure(
            response.get("result"), CustomFieldList
        )
        res = client.custom_fields._last_res
        assert res.url == client._path("custom_field/CODE" + query)


def test_get_specific_custom_field(client):
    response = _status_true(_custom_field())
    with requests_mock.Mocker() as m:
        m.get(client._path("custom_field/CODE/1"), json=response)
        data = client.custom_fields.get("CODE", 1)
        assert data == converter.structure(
            response.get("result"), CustomFieldInfo
        )
        res = client.custom_fields._last_res
        assert res.url == client._path("custom_field/CODE/1")


def test_custom_field_exists(client):
    response = _status_true(_custom_field())
    with requests_mock.Mocker() as m:
        m.get(
            client._path("custom_field/CODE/1"),
            [
                {"status_code": 200, "json": response},
                {"status_code": 404, "json": {}},
            ],
        )
        assert client.custom_fields.exists("CODE", 1)
        assert not client.custom_fields.exists("CODE", 1)
