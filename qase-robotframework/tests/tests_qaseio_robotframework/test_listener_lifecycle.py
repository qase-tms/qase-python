"""Run lifecycle of the Listener across a suite hierarchy, pabot and keywords."""
import json
import os
import subprocess
import sys
from unittest.mock import MagicMock, patch

with patch("robot.libraries.BuiltIn.BuiltIn"):
    from qase.robotframework.listener import Listener


def _suite(name, parent=None, suites=(), tests=()):
    suite = MagicMock(spec=["name", "parent", "suites", "tests"])
    suite.name = name
    suite.parent = parent
    suite.suites = list(suites)
    suite.tests = list(tests)
    return suite


def _listener():
    listener = Listener.__new__(Listener)
    listener.tests = {}
    listener.in_test = False
    listener.reporter = MagicMock()
    listener.reporter.get_execution_plan.return_value = None
    listener.runtime = MagicMock()
    listener.logger = MagicMock()
    return listener


def _start_suite(listener, suite, pool_id=None):
    with patch("qase.robotframework.listener.get_pool_id", return_value=pool_id), \
            patch("qase.robotframework.listener.get_last_level_flag", return_value=None):
        listener.start_suite(suite, MagicMock())


class TestStartRunOnce:

    def test_child_suites_do_not_start_the_run_again(self):
        listener = _listener()
        root = _suite("Tests")
        child = _suite("A", parent=root)

        _start_suite(listener, root)
        _start_suite(listener, child)

        listener.reporter.start_run.assert_called_once()


class TestPabotWait:

    def test_gives_up_waiting_for_run_id(self, tmp_path, monkeypatch):
        monkeypatch.setattr(Listener, "meta_run_file", tmp_path / "src.run")
        monkeypatch.setattr(Listener, "pabot_run_id_timeout", 0.05)
        monkeypatch.setattr(Listener, "pabot_poll_interval", 0.01)
        listener = _listener()

        _start_suite(listener, _suite("Tests"), pool_id="1")

        listener.logger.log_error.assert_called_once()
        listener.reporter.set_run_id.assert_not_called()

    def test_loads_run_id_written_by_first_process(self, tmp_path, monkeypatch):
        run_file = tmp_path / "src.run"
        run_file.write_text("42")
        monkeypatch.setattr(Listener, "meta_run_file", run_file)
        listener = _listener()

        _start_suite(listener, _suite("Tests"), pool_id="1")

        listener.reporter.set_run_id.assert_called_once_with("42")


class TestUserKeywordOutsideTest:

    def _keyword_result(self):
        result = MagicMock()
        result.tags = ["qase.fields:{\"priority\":\"high\"}"]
        return result

    def test_suite_setup_keyword_does_not_touch_runtime(self):
        listener = _listener()
        listener.runtime.result = None

        listener.end_user_keyword(MagicMock(), MagicMock(), self._keyword_result())

    def test_suite_teardown_keyword_does_not_change_reported_result(self):
        listener = _listener()
        reported = MagicMock()
        listener.runtime.result = reported
        listener.in_test = False

        listener.end_user_keyword(MagicMock(), MagicMock(), self._keyword_result())

        reported.add_field.assert_not_called()


ROBOT_TEST = """*** Test Cases ***
Login
    Log    {suite}
"""


class TestRobotRunInReportMode:

    def test_every_suite_is_reported_under_its_own_path(self, tmp_path):
        tests = tmp_path / "tests"
        for suite in ("a", "b"):
            (tests / suite).mkdir(parents=True)
            (tests / suite / "one.robot").write_text(ROBOT_TEST.format(suite=suite))
        env = {**os.environ, "QASE_MODE": "report"}

        subprocess.run(
            [sys.executable, "-m", "robot", "--listener", "qase.robotframework.Listener",
             "--output", "NONE", "--report", "NONE", "--log", "NONE", "tests"],
            cwd=tmp_path, env=env, check=True, capture_output=True,
        )

        results_dir = tmp_path / "build" / "qase-report" / "results"
        suites = sorted(
            [s["title"] for s in json.loads(p.read_text())["relations"]["suite"]["data"]]
            for p in results_dir.iterdir()
        )
        assert suites == [["Tests", "A", "One"], ["Tests", "B", "One"]]
