import pytest

from apitist.hooks import (
    PrepRequestDebugLoggingHook,
    RequestConverterHook,
    ResponseDebugLoggingHook,
)

from qaseio.client import QaseApi


def test_session_hooks():
    client = QaseApi("")
    assert RequestConverterHook in client._s.request_hooks
    assert PrepRequestDebugLoggingHook in client._s.prep_request_hooks
    assert ResponseDebugLoggingHook in client._s.response_hooks


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
