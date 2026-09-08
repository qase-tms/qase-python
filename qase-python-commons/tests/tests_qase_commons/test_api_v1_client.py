from unittest.mock import Mock, patch

import pytest

from qase.commons import retry as retry_module
from qase.commons.client.api_v1_client import ApiV1Client
from qase.commons.models.attachment import Attachment


def _client(timeout: int = 7, retries: int = 3, retry_backoff: int = 1) -> ApiV1Client:
    """An ApiV1Client whose __init__ is bypassed.

    The real __init__ builds an API client and reads certifi; the methods under
    test only need self.client, self.config and self.logger.
    """
    client = ApiV1Client.__new__(ApiV1Client)
    config = Mock()
    config.testops.api.timeout = timeout
    config.testops.api.retries = retries
    config.testops.api.retry_backoff = retry_backoff
    config.testops.configurations.values = []
    config.testops.run.tags = []
    config.testops.run.external_link = None
    client.config = config
    client.logger = Mock()
    client.client = Mock()
    client.web = "https://app.qase.io"
    return client


def _attachment(name: str = "log.txt") -> Attachment:
    return Attachment(file_name=name, mime_type="text/plain", content="content")


def _http_error(status: int) -> Exception:
    error = Exception(f"HTTP {status}")
    error.status = status
    return error


@pytest.fixture(autouse=True)
def _no_backoff_sleep():
    """Keep the retry ladder instant without faking the retry logic itself."""
    with patch.object(retry_module.time, "sleep"):
        yield


def test_upload_attachment_passes_the_configured_timeout():
    client = _client(timeout=7)

    with patch("qase.commons.client.api_v1_client.AttachmentsApi") as attachments_api:
        client._upload_attachment("DEMO", [_attachment()])

    kwargs = attachments_api.return_value.upload_attachment.call_args.kwargs
    assert kwargs["_request_timeout"] == 7


def test_upload_attachment_retries_a_retryable_failure():
    client = _client(retries=3)
    uploaded = Mock()
    response = Mock(result=[uploaded])

    with patch("qase.commons.client.api_v1_client.AttachmentsApi") as attachments_api:
        attachments_api.return_value.upload_attachment.side_effect = [
            TimeoutError("read timed out"),
            response,
        ]
        result = client._upload_attachment("DEMO", [_attachment()])

    assert attachments_api.return_value.upload_attachment.call_count == 2
    assert result == [uploaded]


def test_upload_attachment_stops_after_the_configured_attempts():
    client = _client(retries=2)

    with patch("qase.commons.client.api_v1_client.AttachmentsApi") as attachments_api:
        attachments_api.return_value.upload_attachment.side_effect = TimeoutError(
            "read timed out"
        )
        result = client._upload_attachment("DEMO", [_attachment()])

    assert attachments_api.return_value.upload_attachment.call_count == 2
    assert result == []


def test_upload_attachment_does_not_retry_a_non_retryable_failure():
    client = _client(retries=3)

    with patch("qase.commons.client.api_v1_client.AttachmentsApi") as attachments_api:
        attachments_api.return_value.upload_attachment.side_effect = _http_error(400)
        result = client._upload_attachment("DEMO", [_attachment()])

    assert attachments_api.return_value.upload_attachment.call_count == 1
    assert result == []


def test_upload_attachment_keeps_uploading_after_a_batch_is_exhausted():
    """A batch that cannot be uploaded must not abort the remaining batches."""
    client = _client(retries=2)
    uploaded = Mock()
    # 21 attachments do not fit into one request (20 files max), so they are
    # split into two batches; the first one fails for good.
    attachments = [_attachment(f"log-{i}.txt") for i in range(21)]

    with patch("qase.commons.client.api_v1_client.AttachmentsApi") as attachments_api:
        attachments_api.return_value.upload_attachment.side_effect = [
            TimeoutError("read timed out"),
            TimeoutError("read timed out"),
            Mock(result=[uploaded]),
        ]
        result = client._upload_attachment("DEMO", attachments)

    assert result == [uploaded]


def test_get_project_passes_the_configured_timeout():
    client = _client(timeout=7)

    with patch("qase.commons.client.api_v1_client.ProjectsApi") as projects_api:
        client.get_project("DEMO")

    kwargs = projects_api.return_value.get_project.call_args.kwargs
    assert kwargs["_request_timeout"] == 7


def test_get_environment_passes_the_configured_timeout():
    client = _client(timeout=7)

    with patch("qase.commons.client.api_v1_client.EnvironmentsApi") as environments_api:
        environments_api.return_value.get_environments.return_value = Mock(
            result=Mock(entities=[])
        )
        client.get_environment("staging", "DEMO")

    kwargs = environments_api.return_value.get_environments.call_args.kwargs
    assert kwargs["_request_timeout"] == 7


def test_get_configurations_passes_the_configured_timeout():
    client = _client(timeout=7)

    with patch("qase.commons.client.api_v1_client.ConfigurationsApi") as configurations_api:
        configurations_api.return_value.get_configurations.return_value = Mock(
            result=Mock(entities=[])
        )
        client.get_configurations("DEMO")

    kwargs = configurations_api.return_value.get_configurations.call_args.kwargs
    assert kwargs["_request_timeout"] == 7


def test_create_test_run_passes_the_configured_timeout():
    client = _client(timeout=7)

    with patch("qase.commons.client.api_v1_client.RunsApi") as runs_api:
        client.create_test_run("DEMO", "title", "description")

    kwargs = runs_api.return_value.create_run.call_args.kwargs
    assert kwargs["_request_timeout"] == 7


def test_check_test_run_passes_the_configured_timeout():
    client = _client(timeout=7)

    with patch("qase.commons.client.api_v1_client.RunsApi") as runs_api:
        client.check_test_run("DEMO", 1)

    kwargs = runs_api.return_value.get_run.call_args.kwargs
    assert kwargs["_request_timeout"] == 7


def test_complete_run_passes_the_configured_timeout():
    client = _client(timeout=7)

    with patch("qase.commons.client.api_v1_client.RunsApi") as runs_api:
        runs_api.return_value.get_run.return_value = Mock(result=Mock(status=0))
        client.complete_run("DEMO", 1)

    kwargs = runs_api.return_value.complete_run.call_args.kwargs
    assert kwargs["_request_timeout"] == 7


def test_enable_public_report_passes_the_configured_timeout():
    client = _client(timeout=7)

    with patch("qase.commons.client.api_v1_client.RunsApi") as runs_api:
        client.enable_public_report("DEMO", 1)

    kwargs = runs_api.return_value.update_run_publicity.call_args.kwargs
    assert kwargs["_request_timeout"] == 7


def test_find_or_create_configuration_passes_the_configured_timeout():
    client = _client(timeout=7)
    client.config.testops.configurations.create_if_not_exists = True
    client.get_configurations = Mock(return_value=[])
    config_value = Mock(name_="group", value="value")
    config_value.name = "group"

    with patch("qase.commons.client.api_v1_client.ConfigurationsApi") as configurations_api:
        configurations_api.return_value.create_configuration_group.return_value = Mock(
            result=Mock(id=1)
        )
        client.find_or_create_configuration("DEMO", config_value)

    group_kwargs = configurations_api.return_value.create_configuration_group.call_args.kwargs
    config_kwargs = configurations_api.return_value.create_configuration.call_args.kwargs
    assert group_kwargs["_request_timeout"] == 7
    assert config_kwargs["_request_timeout"] == 7
