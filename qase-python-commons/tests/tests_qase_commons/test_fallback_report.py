"""
The report fallback must end up with every result the TestOps reporter held,
written to disk the same way a report-mode run writes them.
"""
import json
from unittest.mock import Mock, patch

from qase.commons.config import ConfigManager
from qase.commons.models import Result, Run
from qase.commons.reporters.core import QaseCoreReporter
from qase.commons.reporters.report import QaseReport
from qase.commons.reporters.testops import QaseTestOps


def _make_core(tmp_path, mode="testops"):
    config = ConfigManager("/nonexistent/path.json")
    config.config.set_mode(mode)
    config.config.set_fallback("report")
    config.config.testops.api.set_token("tok")
    config.config.testops.set_project("PRJ")
    config.config.testops.plan.id = None
    config.config.report.connection.set_path(str(tmp_path / "report"))
    with patch("qase.commons.reporters.core.get_host_info", return_value={}), \
            patch("qase.commons.client.api_v2_client.ApiV2Client"), \
            patch("qase.commons.reporters.core.QaseTestOps"), \
            patch("qase.commons.reporters.core.QaseTestOpsMulti"):
        core = QaseCoreReporter(config)
    return core


def _result(title):
    result = Result(title=title, signature=title)
    result.execution.set_status("passed")
    return result


def _report_titles(tmp_path):
    assert (tmp_path / "report" / "run.json").exists()
    titles = []
    for path in (tmp_path / "report" / "results").iterdir():
        titles.append(json.loads(path.read_text())["title"])
    return sorted(titles)


def _complete(core):
    with patch("qase.commons.reporters.report.get_host_info", return_value={}):
        core.complete_run()


class TestQaseReportSetResults:

    def test_list_results_are_written_to_results_dir(self, tmp_path):
        core = _make_core(tmp_path, mode="report")
        core.start_run()

        core.reporter.set_results([_result("a"), _result("b")])
        _complete(core)

        titles = _report_titles(tmp_path)
        assert titles == ["a", "b"]

    def test_multi_project_results_are_written_to_results_dir(self, tmp_path):
        core = _make_core(tmp_path, mode="report")
        core.start_run()

        core.reporter.set_results({"P1": [_result("a")], "P2": [_result("b")]})
        _complete(core)

        titles = _report_titles(tmp_path)
        assert titles == ["a", "b"]


class TestFallbackKeepsResults:

    def test_add_result_failure_writes_buffered_results(self, tmp_path):
        core = _make_core(tmp_path)
        testops = core.reporter
        testops.get_results.return_value = [_result("a"), _result("b")]
        testops.add_result.side_effect = Exception("API down")

        core.start_run()
        core.add_result(_result("c"))
        _complete(core)

        assert isinstance(core.reporter, QaseReport)
        titles = _report_titles(tmp_path)
        assert titles == ["a", "b"]

    def test_start_run_failure_switches_to_fallback(self, tmp_path):
        core = _make_core(tmp_path)
        core.reporter.start_run.side_effect = Exception("network down")
        core.reporter.get_results.return_value = []

        core.start_run()
        core.add_result(_result("a"))
        _complete(core)

        assert isinstance(core.reporter, QaseReport)
        titles = _report_titles(tmp_path)
        assert titles == ["a"]

    def test_start_run_failure_without_fallback_disables_reporting(self, tmp_path):
        core = _make_core(tmp_path)
        core.fallback = None
        core.reporter.start_run.side_effect = Exception("network down")

        core.start_run()

        assert core.reporter is None

    def test_fallback_does_not_restart_itself(self, tmp_path):
        # testops init failed, so the fallback is already the active reporter
        core = _make_core(tmp_path, mode="report")
        core.fallback = core.reporter
        core.start_run()
        core.add_result(_result("a"))

        core._run_fallback()
        _complete(core)

        titles = _report_titles(tmp_path)
        assert titles == ["a"]


class TestUndeliveredResults:

    def _testops(self):
        config = ConfigManager("/nonexistent/path.json").config
        config.testops.set_project("PRJ")
        config.testops.api.retries = 1
        config.testops.api.retry_backoff = 0
        client = Mock()
        client.send_results.side_effect = Exception("503")
        reporter = QaseTestOps(config=config, logger=Mock(), client=client)
        reporter.run_id = 1
        return reporter

    def test_undelivered_batch_is_kept_in_results(self):
        reporter = self._testops()
        reporter.add_result(_result("a"))

        reporter.complete_worker()

        assert [r.title for r in reporter.get_results()] == ["a"]
        assert reporter.lost_results == 1

    def test_complete_run_writes_undelivered_results_to_fallback(self, tmp_path):
        core = _make_core(tmp_path)
        core.reporter = self._testops()

        core.add_result(_result("a"))
        _complete(core)

        assert isinstance(core.reporter, QaseReport)
        titles = _report_titles(tmp_path)
        assert titles == ["a"]


class TestRunCompilation:

    def _result_dict(self, relations):
        return {
            "id": "1",
            "title": "a",
            "relations": relations,
            "execution": {"status": "passed", "duration": 1, "thread": "main",
                          "start_time": 1, "end_time": 2},
        }

    def test_result_without_relations_is_added(self):
        run = Run(title="r", start_time=1, end_time=2)

        run.add_result(self._result_dict(None))

        assert [r["title"] for r in run.results] == ["a"]
        assert run.suites == []

    def test_runs_do_not_share_results(self):
        Run(title="r1", start_time=1, end_time=2).add_result(self._result_dict(None))

        assert Run(title="r2", start_time=1, end_time=2).results == []
