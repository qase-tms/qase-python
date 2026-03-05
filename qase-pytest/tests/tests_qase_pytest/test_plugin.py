"""
Tests for QasePytestPlugin edge cases and error scenarios.

Covers marker parsing (qase_id, qase_title, qase_fields, qase_author,
qase_muted, qase_project_id), graceful fallback behavior, and
singleton lifecycle.
"""

import pytest
from unittest.mock import MagicMock, PropertyMock

from qase.pytest.plugin import (
    QasePytestPlugin,
    QasePytestPluginSingleton,
    PluginNotInitializedException,
)


def make_mock_item(
    markers=None,
    nodeid="tests/test_example.py::test_func",
    originalname="test_func",
):
    """Create a mock pytest item with configurable markers."""
    item = MagicMock()
    item.nodeid = nodeid
    item.originalname = originalname

    def get_closest_marker(name):
        if markers and name in markers:
            return markers[name]
        return None

    item.get_closest_marker = MagicMock(side_effect=get_closest_marker)
    item.iter_markers = MagicMock(
        return_value=iter(markers.values() if markers else [])
    )

    # Simulate item without callspec (no parametrize)
    type(item).callspec = PropertyMock(side_effect=AttributeError)
    item._grouped_params = []

    return item


def make_marker(**kwargs):
    """Create a mock pytest marker with given kwargs."""
    marker = MagicMock()
    marker.kwargs = kwargs
    return marker


def make_plugin():
    """Create a QasePytestPlugin with a mock reporter."""
    reporter = MagicMock()
    reporter.config = MagicMock()
    reporter.get_execution_plan.return_value = None
    return QasePytestPlugin(reporter=reporter)


class TestGetQaseIds:
    """Test _get_qase_ids static method edge cases."""

    def test_returns_none_when_no_marker(self):
        item = make_mock_item()
        assert QasePytestPlugin._get_qase_ids(item) is None

    def test_returns_list_with_integer_id(self):
        marker = make_marker(id=42)
        item = make_mock_item(markers={"qase_id": marker})
        assert QasePytestPlugin._get_qase_ids(item) == [42]

    def test_returns_list_from_comma_separated_string(self):
        marker = make_marker(id="1,2,3")
        item = make_mock_item(markers={"qase_id": marker})
        assert QasePytestPlugin._get_qase_ids(item) == [1, 2, 3]

    def test_returns_none_when_id_kwarg_is_none(self):
        marker = make_marker(id=None)
        item = make_mock_item(markers={"qase_id": marker})
        assert QasePytestPlugin._get_qase_ids(item) is None

    def test_handles_string_with_spaces(self):
        marker = make_marker(id="10, 20, 30")
        item = make_mock_item(markers={"qase_id": marker})
        assert QasePytestPlugin._get_qase_ids(item) == [10, 20, 30]

    def test_raises_on_non_numeric_string(self):
        marker = make_marker(id="abc")
        item = make_mock_item(markers={"qase_id": marker})
        with pytest.raises(ValueError):
            QasePytestPlugin._get_qase_ids(item)


class TestGetTitle:
    """Test _get_title instance method edge cases."""

    def test_falls_back_to_originalname_when_no_marker(self):
        plugin = make_plugin()
        item = make_mock_item(originalname="my_test_func")
        assert plugin._get_title(item) == "my_test_func"

    def test_returns_marker_title(self):
        marker = make_marker(title="Custom Title")
        plugin = make_plugin()
        item = make_mock_item(markers={"qase_title": marker})
        assert plugin._get_title(item) == "Custom Title"

    def test_converts_non_string_title_to_str(self):
        marker = make_marker(title=12345)
        plugin = make_plugin()
        item = make_mock_item(markers={"qase_title": marker})
        assert plugin._get_title(item) == "12345"

    def test_falls_back_when_title_kwarg_is_none(self):
        marker = make_marker(title=None)
        plugin = make_plugin()
        item = make_mock_item(
            markers={"qase_title": marker}, originalname="fallback_name"
        )
        # title=None is falsy, so it falls back to originalname
        assert plugin._get_title(item) == "fallback_name"


class TestSetFields:
    """Test _set_fields instance method edge cases."""

    def test_no_crash_when_no_markers(self):
        plugin = make_plugin()
        item = make_mock_item()
        plugin.runtime.result = MagicMock()
        plugin._set_fields(item)
        # Should not raise -- silently skips missing markers

    def test_no_crash_when_qase_fields_has_no_kwargs(self):
        marker = MagicMock()
        marker.kwargs = {}
        plugin = make_plugin()
        item = make_mock_item(markers={"qase_fields": marker})
        plugin.runtime.result = MagicMock()
        # kwargs.get("fields") returns None, iterating None raises TypeError
        # which is caught by except (AttributeError, TypeError)
        plugin._set_fields(item)


class TestSetTestopsIds:
    """Test _set_testops_ids instance method edge cases."""

    def test_no_crash_when_no_markers(self):
        plugin = make_plugin()
        item = make_mock_item()
        # iter_markers returns empty iterator for any marker name
        item.iter_markers = MagicMock(return_value=iter([]))
        plugin.runtime.result = MagicMock()
        plugin._set_testops_ids(item)
        # Should not raise

    def test_no_crash_when_marker_kwargs_are_none(self):
        marker = MagicMock()
        marker.kwargs = {"project_code": None, "testops_ids": None}
        plugin = make_plugin()
        item = make_mock_item()
        item.iter_markers = MagicMock(return_value=iter([marker]))
        plugin.runtime.result = MagicMock()
        plugin._set_testops_ids(item)
        # project_code is None so condition fails -- no crash


class TestSetAuthor:
    """Test _set_author instance method edge cases."""

    def test_no_crash_when_no_marker(self):
        plugin = make_plugin()
        item = make_mock_item()
        plugin.runtime.result = MagicMock()
        plugin._set_author(item)
        # Should not raise


class TestSetMuted:
    """Test _set_muted instance method edge cases."""

    def test_no_crash_when_no_marker(self):
        plugin = make_plugin()
        item = make_mock_item()
        plugin.runtime.result = MagicMock()
        plugin._set_muted(item)
        # Should not raise


class TestQasePytestPluginSingleton:
    """Test singleton lifecycle and error handling."""

    def teardown_method(self):
        QasePytestPluginSingleton._instance = None

    def test_get_instance_raises_when_not_initialized(self):
        QasePytestPluginSingleton._instance = None
        with pytest.raises(PluginNotInitializedException, match="Init plugin first"):
            QasePytestPluginSingleton.get_instance()

    def test_init_creates_instance(self):
        reporter = MagicMock()
        reporter.config = MagicMock()
        reporter.get_execution_plan.return_value = None
        QasePytestPluginSingleton.init(reporter=reporter)
        instance = QasePytestPluginSingleton.get_instance()
        assert isinstance(instance, QasePytestPlugin)

    def test_init_does_not_replace_existing_instance(self):
        reporter1 = MagicMock()
        reporter1.config = MagicMock()
        reporter1.get_execution_plan.return_value = None
        QasePytestPluginSingleton.init(reporter=reporter1)
        first = QasePytestPluginSingleton.get_instance()

        reporter2 = MagicMock()
        reporter2.config = MagicMock()
        reporter2.get_execution_plan.return_value = None
        QasePytestPluginSingleton.init(reporter=reporter2)
        second = QasePytestPluginSingleton.get_instance()

        assert first is second
