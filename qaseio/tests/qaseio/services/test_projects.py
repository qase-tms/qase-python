import json

import pytest

import requests_mock
from apitist.constructor import converter
from tests.data import _list, _project, _status_true

from qaseio.client.models import (
    ProjectCreate,
    ProjectCreated,
    ProjectInfo,
    ProjectList,
)


@pytest.mark.parametrize(
    "params, query",
    [
        ((10, 30), "?limit=10&offset=30"),
        ((None, 30), "?offset=30"),
        ((10, None), "?limit=10"),
    ],
)
def test_get_all_projects(client, params, query):
    response = _status_true(_list(_project()))
    with requests_mock.Mocker() as m:
        m.get(client._path("project"), json=response)
        data = client.projects.get_all(*params)
        assert data == converter.structure(response.get("result"), ProjectList)
        res = client.projects._last_res
        assert res.url == client._path("project" + query)


def test_get_specific_project(client):
    response = _status_true(_project())
    with requests_mock.Mocker() as m:
        m.get(client._path("project/CODE"), json=response)
        data = client.projects.get("CODE")
        assert data == converter.structure(response.get("result"), ProjectInfo)
        res = client.projects._last_res
        assert res.url == client._path("project/CODE")


def test_project_exists(client):
    response = _status_true(_project())
    with requests_mock.Mocker() as m:
        m.get(
            client._path("project/CODE"),
            [
                {"status_code": 200, "json": response},
                {"status_code": 404, "json": {}},
            ],
        )
        assert client.projects.exists("CODE")
        assert not client.projects.exists("CODE")


def test_create_new_project(client):
    response = _status_true({"code": "NEW"})
    with requests_mock.Mocker() as m:
        m.post(client._path("project"), json=response)
        create_data = ProjectCreate("new project", "NEW")
        data = client.projects.create(create_data)
        assert data == converter.structure(
            response.get("result"), ProjectCreated
        )
        res = client.projects._last_res
        assert json.loads(res.request.body) == converter.unstructure(
            create_data
        )
