"""
With qase-pytest active, qase-tavern reports Tavern tests through qase-pytest's
reporter into the same run and leaves the run lifecycle and other tests to it.
"""
from unittest.mock import MagicMock

import pytest

from qase.tavern import conftest
from qase.tavern.plugin import QasePytestPlugin, QasePytestPluginSingleton


@pytest.fixture(autouse=True)
def _reset_singleton():
    # The installed plugin initialises the singleton for this very session.
    QasePytestPluginSingleton._instance = None
    yield
    QasePytestPluginSingleton._instance = None


def _config(qase_pytest=None):
    config = MagicMock()
    config.option.__dict__ = {}
    config.pluginmanager.get_plugin.side_effect = (
        lambda name: qase_pytest if name == "qase-pytest" else None
    )
    return config


def _tavern_item():
    item = MagicMock()
    item.spec = {"test_name": "Get user", "stages": []}
    item.fspath.basename = "test_user.tavern.yaml"
    return item


def _regular_item():
    item = MagicMock(spec=["nodeid", "fspath"])
    item.fspath.basename = "test_regular.py"
    return item


class TestConfigure:

    def test_reuses_qase_pytest_reporter(self):
        qase_pytest = MagicMock(delegates_tavern_items=True)
        config = _config(qase_pytest)

        conftest.pytest_configure(config)

        plugin = QasePytestPluginSingleton.get_instance()
        assert plugin.reporter is qase_pytest.reporter
        assert plugin.owns_run is False
        config.pluginmanager.register.assert_called_once_with(plugin, name="qase-tavern")

    def test_steps_aside_for_qase_pytest_that_reports_tavern_tests_itself(self):
        qase_pytest = MagicMock(spec=["reporter"])
        config = _config(qase_pytest)

        conftest.pytest_configure(config)

        config.pluginmanager.register.assert_not_called()
        assert QasePytestPluginSingleton._instance is None

    def test_runs_on_its_own_without_qase_pytest(self, monkeypatch):
        reporter = MagicMock()
        monkeypatch.setattr(conftest, "QaseCoreReporter", MagicMock(return_value=reporter))
        config = _config()

        conftest.pytest_configure(config)

        plugin = QasePytestPluginSingleton.get_instance()
        assert plugin.reporter is reporter
        assert plugin.owns_run is True


class TestSharedRun:

    def _plugin(self):
        return QasePytestPlugin(reporter=MagicMock(), owns_run=False)

    def test_does_not_start_or_complete_the_run(self):
        plugin = self._plugin()

        plugin.pytest_sessionstart(MagicMock())
        plugin.pytest_sessionfinish(MagicMock(), 0)

        plugin.reporter.start_run.assert_not_called()
        plugin.reporter.complete_worker.assert_not_called()
        plugin.reporter.complete_run.assert_not_called()

    def test_reports_tavern_item(self):
        plugin = self._plugin()

        plugin.pytest_runtest_protocol(_tavern_item())
        plugin.pytest_runtest_logfinish()

        plugin.reporter.add_result.assert_called_once()
        assert plugin.reporter.add_result.call_args[0][0].title == "Get user"

    def test_ignores_regular_item(self):
        plugin = self._plugin()

        plugin.pytest_runtest_protocol(_regular_item())
        plugin.pytest_runtest_logfinish()

        plugin.reporter.add_result.assert_not_called()

    def test_standalone_plugin_still_reports_regular_items(self):
        plugin = QasePytestPlugin(reporter=MagicMock())

        plugin.pytest_runtest_protocol(_regular_item())
        plugin.pytest_runtest_logfinish()

        plugin.reporter.add_result.assert_called_once()
