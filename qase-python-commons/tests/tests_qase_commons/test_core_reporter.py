"""
Tests for QaseCoreReporter covering initialization, fallback logic,
and error classification helpers.
"""
from unittest.mock import patch, Mock, call
from qase.commons.config import ConfigManager
from qase.commons.models.config.qaseconfig import Mode
from qase.commons.reporters.core import (
    QaseCoreReporter,
    _is_auth_error,
    _is_network_error,
)
from qase.commons.exceptions.reporter import ReporterException


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


def _make_config(mode="off", token=None, project=None, fallback=None):
    """Shared helper: create ConfigManager without loading real files."""
    config = ConfigManager("/nonexistent/path.json")
    config.config.set_mode(mode)
    if token:
        config.config.testops.api.set_token(token)
    if project:
        config.config.testops.set_project(project)
    if fallback:
        config.config.set_fallback(fallback)
    config.config.testops.plan.id = None
    return config


class TestCoreReporterFallback:
    """TEST-02: Core reporter fallback logic when testops init fails."""

    @patch("qase.commons.reporters.core.get_host_info", return_value={})
    @patch("qase.commons.client.api_v2_client.ApiV2Client")
    @patch("qase.commons.reporters.core.QaseReport")
    def test_fallback_on_reporter_exception(
        self, mock_report_cls, mock_api_client, mock_host
    ):
        """ReporterException during testops init -> fallback to QaseReport."""
        mock_api_client.side_effect = ReporterException("API init failed")
        config = _make_config(
            "testops", token="tok", project="PRJ", fallback="report"
        )

        reporter = QaseCoreReporter(config)

        # _fallback_setup creates QaseReport first, then testops fails,
        # reporter gets the fallback instance
        assert reporter.reporter is not None
        # QaseReport was called by _fallback_setup
        assert mock_report_cls.call_count >= 1
        assert reporter.reporter is reporter.fallback

    @patch("qase.commons.reporters.core.get_host_info", return_value={})
    @patch("qase.commons.client.api_v2_client.ApiV2Client")
    @patch("qase.commons.reporters.core.QaseReport")
    def test_fallback_on_generic_exception(
        self, mock_report_cls, mock_api_client, mock_host
    ):
        """Generic Exception during testops init -> fallback to QaseReport."""
        mock_api_client.side_effect = Exception("unexpected crash")
        config = _make_config(
            "testops", token="tok", project="PRJ", fallback="report"
        )

        reporter = QaseCoreReporter(config)

        assert reporter.reporter is not None
        assert reporter.reporter is reporter.fallback

    @patch("qase.commons.reporters.core.get_host_info", return_value={})
    @patch("qase.commons.client.api_v2_client.ApiV2Client")
    def test_no_fallback_when_not_configured(self, mock_api_client, mock_host):
        """No fallback configured -> reporter is None after failure."""
        mock_api_client.side_effect = ReporterException("API init failed")
        config = _make_config("testops", token="tok", project="PRJ")
        # fallback defaults to Mode.off -> _fallback_setup returns None

        reporter = QaseCoreReporter(config)

        assert reporter.reporter is None
        assert reporter.fallback is None

    @patch("qase.commons.reporters.core.get_host_info", return_value={})
    @patch("qase.commons.client.api_v2_client.ApiV2Client")
    @patch("qase.commons.reporters.core.QaseReport")
    def test_fallback_on_testops_multi_exception(
        self, mock_report_cls, mock_api_client, mock_host
    ):
        """ReporterException during testops_multi init -> fallback to QaseReport."""
        from qase.commons.models.config.testops import ProjectConfig

        mock_api_client.side_effect = ReporterException("API init failed")
        config = _make_config(
            "testops_multi", token="tok", fallback="report"
        )
        p = ProjectConfig()
        p.set_code("PRJ")
        config.config.testops_multi.set_projects([p])

        reporter = QaseCoreReporter(config)

        assert reporter.reporter is not None
        assert reporter.reporter is reporter.fallback


class TestCoreReporterSetRunId:
    """set_run_id dispatch between single and multi reporters."""

    def _make_reporter_with_inner(self, inner):
        """Build a QaseCoreReporter bypassing __init__ to attach any inner reporter."""
        reporter = QaseCoreReporter.__new__(QaseCoreReporter)
        reporter.reporter = inner
        reporter.fallback = None
        reporter.logger = Mock()
        reporter.overhead = 0.0
        return reporter

    def test_dict_run_id_routes_to_set_run_ids(self):
        """A dict run_id from xdist controller must be applied via set_run_ids."""
        inner = Mock(spec=["set_run_ids", "set_run_id"])
        reporter = self._make_reporter_with_inner(inner)

        reporter.set_run_id({"PROJ1": 111, "PROJ2": 222})

        inner.set_run_ids.assert_called_once_with({"PROJ1": 111, "PROJ2": 222})
        inner.set_run_id.assert_not_called()

    def test_scalar_run_id_routes_to_set_run_id(self):
        """A scalar run_id keeps the single-project code path."""
        inner = Mock(spec=["set_run_id"])
        reporter = self._make_reporter_with_inner(inner)

        reporter.set_run_id("1553")

        inner.set_run_id.assert_called_once_with("1553")

    def test_dict_run_id_falls_back_when_inner_has_no_set_run_ids(self):
        """If inner reporter lacks set_run_ids, the call must not raise — caller never crashes."""
        inner = Mock(spec=["set_run_id"])  # no set_run_ids attribute
        inner.set_run_id.side_effect = TypeError("missing arg")
        reporter = self._make_reporter_with_inner(inner)

        # Should swallow the TypeError just like any other exception
        reporter.set_run_id({"PROJ1": 111})

        inner.set_run_id.assert_called_once()
        reporter.logger.log.assert_any_call("Failed to set run id", "info")


class TestCoreReporterErrorHandling:
    """TEST-03: Error classification helpers and diagnostic logging."""

    # -- _is_auth_error tests --

    def test_is_auth_error_with_401(self):
        assert _is_auth_error(Exception("HTTP 401 Unauthorized")) is True

    def test_is_auth_error_with_403(self):
        assert _is_auth_error(Exception("403 Forbidden")) is True

    def test_is_auth_error_with_unauthorized_string(self):
        assert _is_auth_error(Exception("unauthorized access")) is True

    def test_is_auth_error_with_unrelated(self):
        assert _is_auth_error(Exception("timeout")) is False

    # -- _is_network_error tests --

    def test_is_network_error_with_connection_error(self):
        assert _is_network_error(ConnectionError("refused")) is True

    def test_is_network_error_with_os_error(self):
        assert _is_network_error(OSError("unreachable")) is True

    def test_is_network_error_with_unrelated(self):
        assert _is_network_error(Exception("auth failed")) is False

    # -- Diagnostic log message tests --

    @patch("qase.commons.reporters.core.get_host_info", return_value={})
    @patch("qase.commons.client.api_v2_client.ApiV2Client")
    @patch("qase.commons.reporters.core.QaseReport")
    def test_auth_error_logs_message(
        self, mock_report_cls, mock_api_client, mock_host
    ):
        """Auth error during init logs 'Authentication failed' with host."""
        auth_exc = Exception("HTTP 401 Unauthorized")
        mock_api_client.side_effect = ReporterException(auth_exc)
        config = _make_config(
            "testops", token="tok", project="PRJ", fallback="report"
        )
        # Replace logger.log with a mock to capture calls
        mock_log = Mock()
        config.logger.log = mock_log

        reporter = QaseCoreReporter(config)

        log_messages = [
            str(c.args[0]) for c in mock_log.call_args_list
        ]
        combined = " ".join(log_messages)
        assert "Authentication failed" in combined
        assert config.config.testops.api.host in combined

    @patch("qase.commons.reporters.core.get_host_info", return_value={})
    @patch("qase.commons.client.api_v2_client.ApiV2Client")
    @patch("qase.commons.reporters.core.QaseReport")
    def test_network_error_logs_message(
        self, mock_report_cls, mock_api_client, mock_host
    ):
        """Network error during init logs 'Network error' with host."""
        net_exc = ConnectionError("Connection refused")
        mock_api_client.side_effect = ReporterException(net_exc)
        config = _make_config(
            "testops", token="tok", project="PRJ", fallback="report"
        )
        mock_log = Mock()
        config.logger.log = mock_log

        reporter = QaseCoreReporter(config)

        log_messages = [
            str(c.args[0]) for c in mock_log.call_args_list
        ]
        combined = " ".join(log_messages)
        assert "Network error" in combined
        assert config.config.testops.api.host in combined
