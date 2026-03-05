"""
Tests for behave formatter and utils error scenarios and edge cases.

Covers tag parsing errors (malformed qase.id, missing colon, invalid JSON),
multi-project tags, step status mapping, and scenario field handling.

These tests complement test_utils.py which covers happy paths.
"""

import pytest
from unittest.mock import MagicMock
from qase.commons.models.step import StepType
from qase.behave.utils import parse_scenario, parse_step, filter_scenarios


@pytest.fixture
def mock_scenario():
    def _mock(
        tags, filename="path/to/scenario.feature", name="Scenario Name", row=None
    ):
        scenario = MagicMock()
        scenario.tags = tags
        scenario.filename = filename
        scenario.name = name
        scenario._row = row
        return scenario

    return _mock


class TestTagParsingErrors:
    """Test malformed tag handling in parse_scenario."""

    def test_non_numeric_qase_id_raises_value_error(self, mock_scenario):
        """qase.id:abc should raise ValueError from int() conversion."""
        scenario = mock_scenario(tags=["qase.id:abc"])
        with pytest.raises(ValueError):
            parse_scenario(scenario)

    def test_missing_colon_in_qase_id_raises_index_error(self, mock_scenario):
        """qase.id without colon/value should raise IndexError from split(':')[1]."""
        scenario = mock_scenario(tags=["qase.id"])
        with pytest.raises(IndexError):
            parse_scenario(scenario)

    def test_invalid_json_in_fields_returns_empty_dict(self, mock_scenario):
        """qase.fields:not-json should produce empty fields dict."""
        scenario = mock_scenario(tags=["qase.fields:not-json"])
        result = parse_scenario(scenario)
        assert result.fields == {}

    def test_empty_qase_id_value_raises(self, mock_scenario):
        """qase.id: (colon but no value) should raise ValueError."""
        scenario = mock_scenario(tags=["qase.id:"])
        with pytest.raises(ValueError):
            parse_scenario(scenario)


class TestMultiProjectTags:
    """Test multi-project tag parsing via parse_scenario."""

    def test_single_project_id_tag(self, mock_scenario):
        """qase.project_id.PROJ1:1,2 should set testops_project_mapping."""
        scenario = mock_scenario(tags=["qase.project_id.PROJ1:1,2"])
        result = parse_scenario(scenario)
        # In multi-project mode, testops_ids should be None (not set directly)
        assert result.testops_ids is None
        # Project mapping should be set
        assert result.testops_project_mapping is not None

    def test_multiple_project_id_tags(self, mock_scenario):
        """Multiple project_id tags should create separate mappings."""
        scenario = mock_scenario(
            tags=["qase.project_id.PROJ1:1,2", "qase.project_id.PROJ2:3,4"]
        )
        result = parse_scenario(scenario)
        assert result.testops_ids is None
        assert result.testops_project_mapping is not None


class TestStepParsing:
    """Test parse_step status mapping edge cases."""

    def test_undefined_status_maps_to_skipped(self):
        """Step with status 'undefined' should map to 'skipped'."""
        step = MagicMock()
        step.keyword = "When"
        step.name = "an undefined step"
        step.line = 5
        step.status.name = "undefined"
        step.duration = 0.0

        qase_step = parse_step(step)
        assert qase_step.execution.status == "skipped"

    def test_pending_status_maps_to_skipped(self):
        """Step with status 'pending' should map to 'skipped'."""
        step = MagicMock()
        step.keyword = "Then"
        step.name = "a pending step"
        step.line = 8
        step.status.name = "pending"
        step.duration = 0.0

        qase_step = parse_step(step)
        assert qase_step.execution.status == "skipped"

    def test_failed_status_maps_to_failed(self):
        """Step with status 'failed' should map to 'failed'."""
        step = MagicMock()
        step.keyword = "Then"
        step.name = "a failed step"
        step.line = 12
        step.status.name = "failed"
        step.duration = 1.5

        qase_step = parse_step(step)
        assert qase_step.execution.status == "failed"

    def test_unknown_status_maps_to_skipped(self):
        """An unknown status falls back to 'skipped' via dict.get default."""
        step = MagicMock()
        step.keyword = "Given"
        step.name = "unknown status step"
        step.line = 1
        step.status.name = "some_unknown_status"
        step.duration = 0.0

        qase_step = parse_step(step)
        assert qase_step.execution.status == "skipped"


class TestScenarioFieldHandling:
    """Test scenario-level field parsing in parse_scenario."""

    def test_ignore_tag_sets_ignore_true(self, mock_scenario):
        """qase.ignore tag should set ignore=True on result."""
        scenario = mock_scenario(tags=["qase.ignore"])
        result = parse_scenario(scenario)
        assert result.ignore is True

    def test_suite_tag_with_double_pipe_separator(self, mock_scenario):
        """qase.suite:a||b||c should create 3 suite entries."""
        scenario = mock_scenario(tags=["qase.suite:a||b||c"])
        result = parse_scenario(scenario)
        suite_titles = [s.title for s in result.relations.suite.data]
        assert suite_titles == ["a", "b", "c"]

    def test_no_qase_id_tag_returns_none_testops_ids(self, mock_scenario):
        """Scenario without qase.id tag should have testops_ids=None."""
        scenario = mock_scenario(tags=[])
        result = parse_scenario(scenario)
        assert result.testops_ids is None


class TestFilterScenarios:
    """Test filter_scenarios edge cases."""

    def test_returns_all_scenarios_when_case_ids_empty(self, mock_scenario):
        """Empty case_ids should return all scenarios unfiltered."""
        scenarios = [
            mock_scenario(["qase.id:1"]),
            mock_scenario(["qase.id:2"]),
        ]
        result = filter_scenarios([], scenarios)
        assert result == scenarios

    def test_filters_correctly_by_matching_ids(self, mock_scenario):
        """Only scenarios with matching IDs should be returned."""
        scenarios = [
            mock_scenario(["qase.id:10"]),
            mock_scenario(["qase.id:20"]),
            mock_scenario(["qase.id:30"]),
        ]
        result = filter_scenarios([10, 30], scenarios)
        assert len(result) == 2
        assert result[0].tags == ["qase.id:10"]
        assert result[1].tags == ["qase.id:30"]
