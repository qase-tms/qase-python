from unittest.mock import Mock

import pytest

from qase.commons.client.api_v1_client import ApiV1Client
from qase.commons.client.api_v2_client import ApiV2Client
from qase.commons.util.api_host import get_web_app_url, resolve_cluster_app_url


@pytest.mark.parametrize("host, expected", [
    ("qase.io", "https://app.qase.io"),
    ("eu.qase.io", "https://app-eu.qase.io"),
    ("EU.qase.io", "https://app-eu.qase.io"),
    ("example.qase.io", "https://example.qase.io"),
    # Must not be rewritten to `capp...`: only the cluster table changes the host.
    ("capital.qase.io", "https://capital.qase.io"),
])
def test_get_web_app_url(host, expected):
    assert get_web_app_url(host) == expected


def test_resolve_cluster_app_url_ignores_unknown_hosts():
    assert resolve_cluster_app_url("example.qase.io") is None
    assert resolve_cluster_app_url("qase.io") is None


def _config(host: str) -> Mock:
    config = Mock()
    config.testops.api.host = host
    config.testops.api.token = "token"
    return config


@pytest.mark.parametrize(
    "client_cls, version", [(ApiV1Client, "v1"), (ApiV2Client, "v2")]
)
@pytest.mark.parametrize("host, api_url, web_url", [
    ("qase.io", "https://api.qase.io", "https://app.qase.io"),
    ("eu.qase.io", "https://api-eu.qase.io", "https://app-eu.qase.io"),
    ("example.qase.io", "https://api-example.qase.io", "https://example.qase.io"),
])
def test_clients_point_api_and_web_app_at_the_same_cluster(
    client_cls, version, host, api_url, web_url
):
    client = client_cls(_config(host), Mock())

    assert client.web == web_url
    api = client.client_v2 if version == "v2" else client.client
    assert api.configuration.host == f"{api_url}/{version}"
