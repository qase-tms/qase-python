"""
Tests for QaseCoreReporter covering initialization, fallback logic,
and error classification helpers.
"""
from unittest.mock import patch, Mock
from qase.commons.config import ConfigManager
from qase.commons.models.config.qaseconfig import Mode
from qase.commons.reporters.core import QaseCoreReporter


class TestCoreReporterInit:
    """TEST-01: Core reporter initialization for all four modes."""

    def _make_config(self, mode="off", token=None, project=None):
        """Create ConfigManager without loading real files."""
        config = ConfigManager("/nonexistent/path.json")
        config.config.set_mode(mode)
        if token:
            config.config.testops.api.set_token(token)
        if project:
            config.config.testops.set_project(project)
        # Ensure plan.id is None to skip TestOpsPlanLoader
        config.config.testops.plan.id = None
        return config

    def test_mode_off(self):
        """mode=off: reporter is None."""
        config = self._make_config("off")
        reporter = QaseCoreReporter(config)
        assert reporter.reporter is None

    @patch("qase.commons.reporters.core.QaseReport")
    def test_mode_report(self, mock_report_cls):
        """mode=report: reporter is a QaseReport instance."""
        config = self._make_config("report")
        reporter = QaseCoreReporter(config)
        assert reporter.reporter is mock_report_cls.return_value

    @patch("qase.commons.reporters.core.get_host_info", return_value={})
    @patch("qase.commons.reporters.core.QaseTestOps")
    @patch("qase.commons.client.api_v2_client.ApiV2Client")
    def test_mode_testops(self, mock_api_client, mock_testops_cls, mock_host):
        """mode=testops: reporter is a QaseTestOps instance."""
        config = self._make_config("testops", token="tok", project="PRJ")
        reporter = QaseCoreReporter(config)
        assert reporter.reporter is mock_testops_cls.return_value
        mock_api_client.assert_called_once()

    @patch("qase.commons.reporters.core.get_host_info", return_value={})
    @patch("qase.commons.reporters.core.QaseTestOpsMulti")
    @patch("qase.commons.client.api_v2_client.ApiV2Client")
    def test_mode_testops_multi(
        self, mock_api_client, mock_multi_cls, mock_host
    ):
        """mode=testops_multi: reporter is a QaseTestOpsMulti instance."""
        from qase.commons.models.config.testops import ProjectConfig

        config = self._make_config("testops_multi", token="tok")
        p = ProjectConfig()
        p.set_code("PRJ")
        config.config.testops_multi.set_projects([p])

        reporter = QaseCoreReporter(config)
        assert reporter.reporter is mock_multi_cls.return_value
        mock_api_client.assert_called_once()
