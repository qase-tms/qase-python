import pytest
from unittest.mock import MagicMock
from qase.commons.models.step import StepType
from qase.behave.utils import (
    filter_scenarios, parse_scenario, parse_step, __extract_fields,
    parse_scenario_from_json, parse_step_from_json,
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


def test_parse_scenario_with_qase_tags(mock_scenario):
    scenario = mock_scenario(tags=["qase.id:801", "qase.tags:smoke,regression"])
    result = parse_scenario(scenario)
    assert result.tags == ["smoke", "regression"]


def test_parse_scenario_with_tags_trimmed(mock_scenario):
    scenario = mock_scenario(tags=["qase.tags: smoke , regression "])
    result = parse_scenario(scenario)
    assert result.tags == ["smoke", "regression"]


def test_parse_scenario_with_tags_case_insensitive(mock_scenario):
    scenario = mock_scenario(tags=["QASE.TAGS:Smoke"])
    result = parse_scenario(scenario)
    assert result.tags == ["Smoke"]


def test_parse_scenario_with_multiple_tags_accumulated(mock_scenario):
    scenario = mock_scenario(tags=["qase.tags:smoke", "qase.tags:regression"])
    result = parse_scenario(scenario)
    assert "smoke" in result.tags
    assert "regression" in result.tags


def test_parse_scenario_without_tags_has_empty_list(mock_scenario):
    scenario = mock_scenario(tags=["qase.id:100"])
    result = parse_scenario(scenario)
    assert result.tags == []


class TestParseScenarioFromJson:
    """Tests for parse_scenario_from_json(scenario_dict, feature_filename)."""

    def test_basic_scenario(self):
        scenario_dict = {
            'name': 'Login with valid credentials',
            'status': 'passed',
            'duration': 1.5,
            'tags': [],
        }
        result = parse_scenario_from_json(scenario_dict, 'features/login.feature')
        assert result.title == 'Login with valid credentials'
        assert result.execution.status == 'passed'
        assert result.execution.duration == 1500
        # Without start/stop, end_time should be set and start_time calculated
        assert result.execution.end_time > 0
        assert result.execution.start_time > 0
        assert result.execution.start_time <= result.execution.end_time

    def test_failed_scenario_with_error(self):
        scenario_dict = {
            'name': 'Failing test',
            'status': 'failed',
            'duration': 0.3,
            'tags': [],
            'error_msg': ['AssertionError: expected True', 'got False'],
        }
        result = parse_scenario_from_json(scenario_dict, 'features/test.feature')
        assert result.execution.status == 'failed'
        assert 'AssertionError: expected True' in result.execution.stacktrace
        assert 'got False' in result.execution.stacktrace

    def test_error_scenario_maps_to_invalid(self):
        scenario_dict = {
            'name': 'Error test',
            'status': 'error',
            'duration': 0.1,
            'tags': [],
        }
        result = parse_scenario_from_json(scenario_dict, 'features/test.feature')
        assert result.execution.status == 'invalid'

    def test_qase_id_tag_parsing(self):
        scenario_dict = {
            'name': 'Tagged test',
            'status': 'passed',
            'duration': 0.5,
            'tags': ['qase.id:42'],
        }
        result = parse_scenario_from_json(scenario_dict, 'features/test.feature')
        assert result.testops_ids == [42]

    def test_multiple_qase_tags(self):
        scenario_dict = {
            'name': 'Multi-tag test',
            'status': 'passed',
            'duration': 0.5,
            'tags': [
                'qase.id:10',
                'qase.suite:Auth||Login',
                'qase.fields:{"priority":"high"}',
                'qase.tags:smoke,regression',
            ],
        }
        result = parse_scenario_from_json(scenario_dict, 'features/test.feature')
        assert result.testops_ids == [10]
        assert len(result.relations.suite.data) == 2
        assert result.relations.suite.data[0].title == 'Auth'
        assert result.relations.suite.data[1].title == 'Login'
        assert result.fields.get('priority') == 'high'
        assert 'smoke' in result.tags
        assert 'regression' in result.tags

    def test_multi_project_tags(self):
        scenario_dict = {
            'name': 'Multi-project test',
            'status': 'passed',
            'duration': 0.5,
            'tags': ['qase.project_id.PROJ1:1,2'],
        }
        result = parse_scenario_from_json(scenario_dict, 'features/test.feature')
        mapping = result.get_testops_project_mapping()
        assert mapping is not None
        assert mapping['PROJ1'] == [1, 2]

    def test_ignore_tag(self):
        scenario_dict = {
            'name': 'Ignored test',
            'status': 'passed',
            'duration': 0.1,
            'tags': ['qase.ignore'],
        }
        result = parse_scenario_from_json(scenario_dict, 'features/test.feature')
        assert result.ignore is True

    def test_scenario_outline_parameters(self):
        scenario_dict = {
            'name': 'Parameterized test',
            'status': 'passed',
            'duration': 0.2,
            'tags': [],
            'parameters': {'username': 'admin', 'password': 'secret'},
        }
        result = parse_scenario_from_json(scenario_dict, 'features/test.feature')
        assert result.params == {'username': 'admin', 'password': 'secret'}

    def test_suite_from_filename_when_no_suite_tag(self):
        scenario_dict = {
            'name': 'Suite from path',
            'status': 'passed',
            'duration': 0.1,
            'tags': [],
        }
        result = parse_scenario_from_json(scenario_dict, 'features/auth/login.feature')
        suite_titles = [s.title for s in result.relations.suite.data]
        assert 'features' in suite_titles
        assert 'auth' in suite_titles
        assert 'login.feature' in suite_titles

    def test_timestamps_calculated_from_duration(self):
        """Timestamps should be calculated from current time and duration."""
        scenario_dict = {
            'name': 'Timed test',
            'status': 'passed',
            'duration': 2.0,
            'tags': [],
        }
        result = parse_scenario_from_json(scenario_dict, 'features/test.feature')
        assert result.execution.end_time > 0
        assert result.execution.start_time > 0
        assert abs(result.execution.end_time - result.execution.start_time - 2.0) < 0.1

    def test_thread_from_worker_id(self):
        scenario_dict = {
            'name': 'Parallel test',
            'status': 'passed',
            'duration': 0.5,
            'tags': [],
            'worker_id': '2',
        }
        result = parse_scenario_from_json(scenario_dict, 'features/test.feature')
        assert result.execution.thread == 'worker-2'

    def test_skipped_undefined_untested_statuses(self):
        for status in ['skipped', 'undefined', 'untested']:
            scenario_dict = {
                'name': f'{status} test',
                'status': status,
                'duration': 0.0,
                'tags': [],
            }
            result = parse_scenario_from_json(scenario_dict, 'features/test.feature')
            assert result.execution.status == 'skipped', (
                f"Status '{status}' should map to 'skipped', got '{result.execution.status}'"
            )


class TestParseStepFromJson:
    """Tests for parse_step_from_json(step_dict)."""

    def test_basic_passed_step(self):
        step_dict = {
            'step_type': 'given',
            'name': 'a user exists',
            'line': 5,
            'status': 'passed',
            'duration': 0.5,
        }
        step = parse_step_from_json(step_dict)
        assert step.data.keyword == 'given'
        assert step.data.name == 'a user exists'
        assert step.data.line == 5
        assert step.execution.status == 'passed'
        assert step.execution.duration == 500
        # Without start/stop, times should be calculated
        assert step.execution.end_time > 0
        assert step.execution.start_time > 0
        assert step.execution.start_time <= step.execution.end_time

    def test_failed_step(self):
        step_dict = {
            'step_type': 'then',
            'name': 'it should fail',
            'line': 10,
            'status': 'failed',
            'duration': 0.1,
        }
        step = parse_step_from_json(step_dict)
        assert step.execution.status == 'failed'

    def test_error_step_maps_to_failed(self):
        step_dict = {
            'step_type': 'when',
            'name': 'an error occurs',
            'line': 7,
            'status': 'error',
            'duration': 0.2,
        }
        step = parse_step_from_json(step_dict)
        assert step.execution.status == 'failed'

    def test_undefined_step_maps_to_skipped(self):
        step_dict = {
            'step_type': 'given',
            'name': 'an undefined step',
            'line': 3,
            'status': 'undefined',
            'duration': 0.0,
        }
        step = parse_step_from_json(step_dict)
        assert step.execution.status == 'skipped'

    def test_step_with_duration(self):
        """Step timestamps calculated from current time and duration."""
        step_dict = {
            'step_type': 'given',
            'name': 'timed step',
            'line': 1,
            'status': 'passed',
            'duration': 1.0,
        }
        step = parse_step_from_json(step_dict)
        assert step.execution.end_time > 0
        assert step.execution.start_time > 0
        assert abs(step.execution.end_time - step.execution.start_time - 1.0) < 0.1

    def test_step_defaults(self):
        step_dict = {}
        step = parse_step_from_json(step_dict)
        assert step.data.keyword == 'given'
        assert step.data.name == ''
        assert step.data.line == 0
        assert step.step_type == StepType.GHERKIN
