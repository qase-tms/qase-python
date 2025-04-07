import pytest
from unittest.mock import MagicMock
from qase.commons.models.step import StepType
from qase.behave.utils import (
    filter_scenarios, parse_scenario, parse_step, __extract_fields
)


@pytest.fixture
def mock_scenario():
    def _mock(tags, filename="path/to/scenario.feature", name="Scenario Name", row=None):
        scenario = MagicMock()
        scenario.tags = tags
        scenario.filename = filename
        scenario.name = name
        scenario._row = row
        return scenario

    return _mock


def test_filter_scenarios_with_matching_ids(mock_scenario):
    scenarios = [mock_scenario(["qase.id:1"]), mock_scenario(["qase.id:2"]), mock_scenario(["qase.id:3"])]
    filtered = filter_scenarios([1, 3], scenarios)
    assert len(filtered) == 2
    assert filtered[0].tags == ["qase.id:1"]
    assert filtered[1].tags == ["qase.id:3"]


def test_filter_scenarios_without_matching_ids(mock_scenario):
    scenarios = [mock_scenario(["qase.id:4"]), mock_scenario(["qase.id:5"])]
    filtered = filter_scenarios([1, 2, 3], scenarios)
    assert len(filtered) == 0


def test_filter_scenarios_with_empty_ids(mock_scenario):
    scenarios = [mock_scenario(["qase.id:1"]), mock_scenario(["qase.id:2"])]
    filtered = filter_scenarios([], scenarios)
    assert filtered == scenarios


def test_parse_scenario_with_tags(mock_scenario):
    scenario = mock_scenario(
        tags=["qase.id:123", "qase.fields:{\"key\":\"value\"}", "qase.suite:suite1||suite2"]
    )
    result = parse_scenario(scenario)
    assert result.testops_ids == [123]
    assert result.fields == {"key": "value"}
    assert len(result.relations.suite.data) == 2
    assert result.relations.suite.data[0].title == "suite1"


def test_parse_scenario_without_tags(mock_scenario):
    scenario = mock_scenario(tags=[])
    result = parse_scenario(scenario)
    assert result.testops_ids is None
    assert result.fields == {}
    assert len(result.relations.suite.data) == 3


def test_parse_step():
    step = MagicMock()
    step.keyword = "Given"
    step.name = "a test step"
    step.line = 10
    step.status.name = "passed"

    qase_step = parse_step(step)
    assert qase_step.step_type == StepType.GHERKIN
    assert qase_step.data.keyword == "Given"
    assert qase_step.data.name == "a test step"
    assert qase_step.data.line == 10
    assert qase_step.execution.status == "passed"


def test_extract_fields_valid_json():
    tag = 'qase.fields:{"key_one": "value_one", "key_two": "value_two"}'
    fields = __extract_fields(tag)
    assert fields == {"key_one": "value one", "key_two": "value two"}


def test_extract_fields_invalid_json():
    tag = 'qase.fields:invalid-json'
    fields = __extract_fields(tag)
    assert fields == {}
