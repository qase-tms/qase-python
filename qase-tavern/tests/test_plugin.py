"""Tests for Tavern QasePytestPlugin error scenarios and edge cases.

Supplements test_extractor.py (happy path) with error paths, multi-project
handling, and edge cases for _get_title, _set_relations, and _set_steps.
"""

from unittest.mock import MagicMock, patch

import pytest

from qase.commons.models import Result
from qase.tavern.plugin import QasePytestPlugin, QasePytestPluginSingleton


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(autouse=True)
def _reset_singleton():
    """Ensure singleton is reset after each test."""
    yield
    QasePytestPluginSingleton._instance = None


def _make_plugin(with_result=False):
    """Create a QasePytestPlugin with a mock reporter.

    Args:
        with_result: If True, initialise runtime.result so that instance
            methods like _set_relations and _set_steps can access it.
    """
    reporter = MagicMock()
    reporter.config = MagicMock()
    plugin = QasePytestPlugin(reporter=reporter)
    if with_result:
        plugin.runtime.result = Result(title="test", signature="test")
    return plugin


# ---------------------------------------------------------------------------
# extract_qase_ids -- error paths
# ---------------------------------------------------------------------------


class TestExtractQaseIdsErrors:
    """Error paths for extract_qase_ids (non-string inputs)."""

    def test_int_input_raises_value_error(self):
        with pytest.raises(ValueError, match="Expected a string"):
            QasePytestPlugin.extract_qase_ids(123)

    def test_none_input_raises_value_error(self):
        with pytest.raises(ValueError, match="Expected a string"):
            QasePytestPlugin.extract_qase_ids(None)

    def test_list_input_raises_value_error(self):
        with pytest.raises(ValueError, match="Expected a string"):
            QasePytestPlugin.extract_qase_ids([1, 2])

    def test_empty_string_returns_empty(self):
        qase_ids, project_ids, remaining = QasePytestPlugin.extract_qase_ids("")
        assert qase_ids == []
        assert project_ids == {}
        assert remaining == ""

    def test_no_matching_pattern_returns_original_text(self):
        text = "No IDs here"
        qase_ids, project_ids, remaining = QasePytestPlugin.extract_qase_ids(text)
        assert qase_ids == []
        assert project_ids == {}
        assert remaining == "No IDs here"


# ---------------------------------------------------------------------------
# extract_qase_ids -- multi-project
# ---------------------------------------------------------------------------


class TestExtractQaseIdsMultiProject:
    """Multi-project ID extraction tests."""

    def test_multiple_project_ids(self):
        text = "QaseProjectID.PROJ1=1,2 QaseProjectID.PROJ2=3"
        qase_ids, project_ids, remaining = QasePytestPlugin.extract_qase_ids(text)
        assert qase_ids == []
        assert project_ids == {"PROJ1": [1, 2], "PROJ2": [3]}

    def test_project_ids_take_precedence_over_qase_ids(self):
        """When both QaseProjectID and QaseID present, qase_ids stays empty."""
        text = "QaseProjectID.PROJ1=10 QaseID=99"
        qase_ids, project_ids, remaining = QasePytestPlugin.extract_qase_ids(text)
        assert qase_ids == []
        assert project_ids == {"PROJ1": [10]}

    def test_single_project_multiple_ids(self):
        text = "QaseProjectID.MYPROJ=100,200,300"
        qase_ids, project_ids, remaining = QasePytestPlugin.extract_qase_ids(text)
        assert project_ids == {"MYPROJ": [100, 200, 300]}
        assert qase_ids == []


# ---------------------------------------------------------------------------
# _get_title -- static method
# ---------------------------------------------------------------------------


class TestGetTitle:
    """Tests for _get_title static method."""

    def test_item_with_spec_returns_test_name(self):
        item = MagicMock()
        item.spec = {"test_name": "my_test_case"}
        assert QasePytestPlugin._get_title(item) == "my_test_case"

    def test_item_without_spec_returns_empty_string(self):
        item = MagicMock(spec=[])  # MagicMock spec=[] makes hasattr(item, "spec") False
        del item.spec
        assert QasePytestPlugin._get_title(item) == ""


# ---------------------------------------------------------------------------
# _set_relations -- instance method
# ---------------------------------------------------------------------------


class TestSetRelations:
    """Tests for _set_relations with missing fspath."""

    def test_item_with_fspath_creates_relation(self):
        plugin = _make_plugin(with_result=True)
        item = MagicMock()
        item.fspath.basename = "test_suite.yaml"
        plugin._set_relations(item)
        assert plugin.runtime.result.relations is not None

    def test_item_without_fspath_no_crash(self):
        """Item without fspath attribute should not crash."""
        plugin = _make_plugin(with_result=True)
        item = MagicMock(spec=[])
        del item.fspath
        # Should not raise
        plugin._set_relations(item)

    def test_item_fspath_without_basename_no_crash(self):
        """Item with fspath but no basename should not crash."""
        plugin = _make_plugin(with_result=True)
        item = MagicMock()
        del item.fspath.basename
        # Should not raise
        plugin._set_relations(item)


# ---------------------------------------------------------------------------
# _set_steps -- instance method
# ---------------------------------------------------------------------------


class TestSetSteps:
    """Tests for _set_steps edge cases."""

    def test_item_without_spec_no_crash(self):
        """Item without spec attribute should not crash."""
        plugin = _make_plugin(with_result=True)
        item = MagicMock(spec=[])
        del item.spec
        # Should not raise
        plugin._set_steps(item)

    def test_item_with_spec_iterates_stages(self):
        """Item with spec and stages should iterate through stages.

        NOTE: The actual __prepare_step accesses step.attachments which
        doesn't exist on the Step model (it lives on step.execution).
        This is a pre-existing issue in the plugin. Here we verify _set_steps
        at least enters the loop by checking the call count on add_step.
        """
        plugin = _make_plugin(with_result=True)
        plugin.runtime = MagicMock()
        item = MagicMock()
        item.spec = {
            "stages": [
                {
                    "name": "Login request",
                    "request": {"url": "/api/login", "method": "POST"},
                    "response": {"status_code": 200},
                },
            ]
        }
        # __prepare_step is private, so we need to patch the step creation
        # to avoid the attachments AttributeError
        with patch.object(
            QasePytestPlugin,
            "_QasePytestPlugin__prepare_step",
            return_value=MagicMock(),
        ):
            plugin._set_steps(item)
        plugin.runtime.add_step.assert_called_once()
