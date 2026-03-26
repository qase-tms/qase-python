"""Tests for User-Agent header on API V2 client."""
import re
from unittest.mock import patch

from qase.api_client_v2.api_client import ApiClient


class TestUserAgentHeader:

    def test_user_agent_contains_qase_api_client(self):
        """User-Agent must contain 'qase-api-client' substring."""
        client = ApiClient()
        assert "qase-api-client" in client.user_agent

    def test_user_agent_format(self):
        """User-Agent must match qase-api-client-python/<version>."""
        client = ApiClient()
        assert re.match(r"qase-api-client-python/.+", client.user_agent)

    def test_user_agent_backend_regex_matches(self):
        """Backend regex /qase-api-client[\\w-]*/i must match."""
        client = ApiClient()
        match = re.search(r"qase-api-client[\w-]*", client.user_agent, re.IGNORECASE)
        assert match is not None
        assert match.group(0) == "qase-api-client-python"

    def test_user_agent_version_is_dynamic(self):
        """User-Agent version must come from importlib.metadata, not hardcoded."""
        client = ApiClient()
        version = client.user_agent.split("/")[1]
        assert version != "1.0.0", "Version should not be the old OpenAPI-Generator default"
        assert version != "", "Version should not be empty"

    @patch("importlib.metadata.version", side_effect=Exception("not installed"))
    def test_user_agent_fallback_on_missing_metadata(self, mock_version):
        """When package metadata is unavailable, version falls back to 'unknown'."""
        client = ApiClient()
        assert client.user_agent == "qase-api-client-python/unknown"
