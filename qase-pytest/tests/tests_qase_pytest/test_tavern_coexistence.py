"""
With qase-tavern installed alongside, its YAML tests are reported by qase-tavern
into the same run, so qase-pytest must leave them alone.
"""
from unittest.mock import MagicMock, PropertyMock

from qase.pytest import conftest
from qase.pytest.plugin import QasePytestPlugin


def _plugin(execution_plan=None):
    reporter = MagicMock()
    reporter.get_execution_plan.return_value = execution_plan
    return QasePytestPlugin(reporter=reporter)


def _item(is_tavern, tavern_plugin_active=True):
    item = MagicMock()
    item.nodeid = "tests/test_example.py::test_func"
    item.originalname = "test_func"
    type(item).callspec = PropertyMock(side_effect=AttributeError)
    item._grouped_params = []
    item.iter_markers.return_value = iter([])
    item.get_closest_marker.return_value = None
    tavern = None
    if tavern_plugin_active:
        tavern = MagicMock()
        tavern.handles.side_effect = lambda i: i is item and is_tavern
    item.config.pluginmanager.get_plugin.side_effect = (
        lambda name: tavern if name == "qase-tavern" else None
    )
    return item


def _run_protocol(plugin, item):
    hook = plugin.pytest_runtest_protocol(item)
    next(hook)
    return hook


def test_declares_that_it_delegates_tavern_items():
    assert QasePytestPlugin.delegates_tavern_items is True


def test_tavern_item_is_left_to_qase_tavern():
    plugin = _plugin()
    item = _item(is_tavern=True)

    _run_protocol(plugin, item)

    assert plugin.ignore is True
    assert plugin.runtime.result is None


def test_regular_item_is_reported_when_qase_tavern_is_active():
    plugin = _plugin()
    item = _item(is_tavern=False)

    _run_protocol(plugin, item)

    assert plugin.ignore is False
    assert plugin.runtime.result is not None


def test_execution_plan_keeps_tavern_items():
    plugin = _plugin(execution_plan=[1])
    tavern_item = _item(is_tavern=True)
    regular_item = _item(is_tavern=False, tavern_plugin_active=False)
    items = [tavern_item, regular_item]

    plugin.pytest_collection_modifyitems(MagicMock(), MagicMock(), items)

    assert items == [tavern_item]


def test_unconfigure_unregisters_plugin():
    plugin = object()
    config = MagicMock()
    config.qase = plugin

    conftest.pytest_unconfigure(config)

    config.pluginmanager.unregister.assert_called_once_with(plugin)
    assert not hasattr(config, "qase")
