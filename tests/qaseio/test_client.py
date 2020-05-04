import time

import pytest

import requests_mock
from apitist.constructor import converter
from apitist.hooks import (
    PrepRequestDebugLoggingHook,
    RequestConverterHook,
    ResponseDebugLoggingHook,
)
from tests.data import _project, _status_true

from qaseio.client import QaseApi
from qaseio.client.models import ProjectInfo


def test_session_hooks():
    client = QaseApi("")
    assert RequestConverterHook in client._s.request_hooks
    assert PrepRequestDebugLoggingHook in client._s.prep_request_hooks
    assert ResponseDebugLoggingHook in client._s.response_hooks


def test_retry_request_after(client):
    response = _status_true(_project())
    with requests_mock.Mocker() as m:
        m.get(
            client._path("project/CODE"),
            [
                {"status_code": 429, "headers": {"Retry-After": "5"}},
                {"status_code": 200, "json": response},
            ],
        )
        start_time = time.time()
        data = client.projects.get("CODE")
        stop_time = time.time()
        assert (stop_time - start_time) >= 5
        assert data == converter.structure(response.get("result"), ProjectInfo)


@pytest.mark.parametrize(
    "path, result",
    [
        (None, "https://api.qase.io/v1/"),
        ([], "https://api.qase.io/v1/"),
        ({}, "https://api.qase.io/v1/"),
        ("", "https://api.qase.io/v1/"),
        ("base", "https://api.qase.io/v1/base"),
        ("base/", "https://api.qase.io/v1/base/"),
        ("/base", "https://api.qase.io/v1/base"),
        ("/base/some/123/", "https://api.qase.io/v1/base/some/123/"),
    ],
)
def test_path_func(path, result):
    client = QaseApi("")
    assert client._path(path) == result
