import pytest

import requests_mock
from apitist.constructor import converter
from tests.data import _list, _status_true, _user

from qaseio.client.models import UserInfo, UserList


@pytest.mark.parametrize(
    "params, query",
    [
        ((10, 30), "?limit=10&offset=30"),
        ((None, 30), "?offset=30"),
        ((10, None), "?limit=10"),
    ],
)
def test_get_all_users(client, params, query):
    response = _status_true(_list(_user()))
    with requests_mock.Mocker() as m:
        m.get(client._path("user"), json=response)
        data = client.users.get_all(*params)
        assert data == converter.structure(response.get("result"), UserList)
        res = client.users._last_res
        assert res.url == client._path("user" + query)


def test_get_specific_user(client):
    response = _status_true(_user())
    with requests_mock.Mocker() as m:
        m.get(client._path("user/1"), json=response)
        data = client.users.get(1)
        assert data == converter.structure(response.get("result"), UserInfo)
        res = client.users._last_res
        assert res.url == client._path("user/1")


def test_user_exists(client):
    response = _status_true(_user())
    with requests_mock.Mocker() as m:
        m.get(
            client._path("user/1"),
            [
                {"status_code": 200, "json": response},
                {"status_code": 404, "json": {}},
            ],
        )
        assert client.users.exists(1)
        assert not client.users.exists(1)
