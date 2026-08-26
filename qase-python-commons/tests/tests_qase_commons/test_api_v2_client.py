from unittest.mock import Mock, patch

from qase.commons.client.api_v2_client import ApiV2Client
from qase.commons.models.result import Result


def _client() -> ApiV2Client:
    """An ApiV2Client whose __init__ is bypassed.

    _prepare_result only touches self.config and self.logger, so building the
    real client (which constructs API clients and reads certifi) is unnecessary.
    """
    client = ApiV2Client.__new__(ApiV2Client)
    config = Mock()
    config.exclude_params = []
    config.testops.defect = False
    config.root_suite = None
    client.config = config
    client.logger = Mock()
    return client


def _result(title: str, signature: str) -> Result:
    result = Result(title=title, signature=signature)
    result.execution.set_status("passed")
    return result


def test_prepare_result_sends_the_result_id_as_idempotency_key():
    result = _result("test something", "sig-1")
    prepared = _client()._prepare_result("DEMO", result)
    assert prepared.id == result.id


def test_prepare_result_ids_differ_between_results():
    client = _client()
    first = client._prepare_result("DEMO", _result("a", "s-a"))
    second = client._prepare_result("DEMO", _result("b", "s-b"))
    assert first.id != second.id
