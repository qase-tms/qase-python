from unittest.mock import Mock, patch

from qase.commons.client.api_v2_client import ApiV2Client
from qase.api_client_v2.models.result_step_status import ResultStepStatus
from qase.commons.models.result import Result
from qase.commons.models.step import Step, StepTextData, StepType


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


def test_send_results_passes_the_configured_timeout():
    client = _client()
    client.config.testops.api.timeout = 7
    client.client_v2 = Mock()
    client._prepare_result = Mock(return_value=Mock())

    with patch("qase.commons.client.api_v2_client.ResultsApi") as results_api, patch(
        "qase.commons.client.api_v2_client.CreateResultsRequestV2"
    ):
        client.send_results("DEMO", "1", [Mock()])

    kwargs = results_api.return_value.create_results_v2.call_args.kwargs
    assert kwargs["_request_timeout"] == 7


def _result_with_step(status: str) -> Result:
    result = _result("test something", "sig-1")
    step = Step(step_type=StepType.TEXT, id=None, data=StepTextData(action="do it"))
    step.execution.set_status(status)
    result.add_steps([step])
    return result


def test_invalid_step_is_sent_as_failed():
    # The API has no "invalid" step status and rejects the whole batch on it.
    prepared = _client()._prepare_result("DEMO", _result_with_step("invalid"))

    assert prepared.steps[0].execution.status == ResultStepStatus.FAILED


def test_untested_step_is_sent_as_skipped():
    prepared = _client()._prepare_result("DEMO", _result_with_step("untested"))

    assert prepared.steps[0].execution.status == ResultStepStatus.SKIPPED
