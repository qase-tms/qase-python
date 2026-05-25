"""Tests for Listener static helper methods.

Only tests static/class methods that do NOT require Robot Framework runtime
or ConfigManager/QaseCoreReporter initialization.
"""

from datetime import datetime, timedelta, timezone
from unittest.mock import patch, MagicMock

import pytest

# Patch BuiltIn at import time so Listener module can be loaded
# without a running Robot Framework instance.
with patch("robot.libraries.BuiltIn.BuiltIn"):
    from qase.robotframework.listener import Listener


class TestCreateGherkinStepWithType:
    """Tests for Listener._create_gherkin_step_with_type."""

    def test_creates_step_with_type_as_keyword(self):
        body_element = MagicMock()
        body_element.type = "IF"
        step = Listener._create_gherkin_step_with_type(body_element)
        assert step.data.keyword == "IF"
        assert step.data.name == "IF"
        assert step.data.line == 0

    def test_creates_step_with_else_type(self):
        body_element = MagicMock()
        body_element.type = "ELSE"
        step = Listener._create_gherkin_step_with_type(body_element)
        assert step.data.keyword == "ELSE"


class TestCreateGherkinStepFromName:
    """Tests for Listener._create_gherkin_step_from_name."""

    def test_creates_step_with_name_as_keyword(self):
        body_element = MagicMock()
        body_element.name = "Log To Console"
        step = Listener._create_gherkin_step_from_name(body_element)
        assert step.data.keyword == "Log To Console"
        assert step.data.name == "Log To Console"
        assert step.data.line == 0


class TestSetStepStatusBasedOnChildren:
    """Tests for Listener._set_step_status_based_on_children."""

    def test_all_children_skipped_sets_skipped(self):
        step = MagicMock()
        child1 = MagicMock()
        child1.execution.status = "skipped"
        child2 = MagicMock()
        child2.execution.status = "skipped"

        Listener._set_step_status_based_on_children(step, [child1, child2])
        step.execution.set_status.assert_called_once_with("skipped")

    def test_any_child_not_skipped_sets_passed(self):
        step = MagicMock()
        child1 = MagicMock()
        child1.execution.status = "passed"
        child2 = MagicMock()
        child2.execution.status = "skipped"

        Listener._set_step_status_based_on_children(step, [child1, child2])
        step.execution.set_status.assert_called_once_with("passed")

    def test_single_passed_child_sets_passed(self):
        step = MagicMock()
        child1 = MagicMock()
        child1.execution.status = "passed"

        Listener._set_step_status_based_on_children(step, [child1])
        step.execution.set_status.assert_called_once_with("passed")

    def test_single_failed_child_sets_passed(self):
        """A failed child is not skipped, so result should be passed."""
        step = MagicMock()
        child1 = MagicMock()
        child1.execution.status = "failed"

        Listener._set_step_status_based_on_children(step, [child1])
        step.execution.set_status.assert_called_once_with("passed")


def _make_test(name, lineno):
    test = MagicMock(spec=["name", "lineno"])
    test.name = name
    test.lineno = lineno
    return test


def _make_suite(name, parent=None, suites=None, tests=None):
    """Build a Robot Framework-like Suite mock with parent/suites/tests."""
    suite = MagicMock(spec=["name", "parent", "suites", "tests"])
    suite.name = name
    suite.parent = parent
    suite.suites = suites or []
    suite.tests = tests or []
    return suite


def _bare_listener():
    """Create a Listener instance without running __init__."""
    listener = Listener.__new__(Listener)
    listener.tests = {}
    return listener


class TestExtractTestsWithSuites:
    """Tests for Listener.__extract_tests_with_suites tree walk."""

    def _extract(self, listener, suite):
        return listener._Listener__extract_tests_with_suites(suite)

    def test_flat_suite_with_tests(self):
        listener = _bare_listener()
        suite = _make_suite("Root", tests=[_make_test("test_one", 1)])

        result = self._extract(listener, suite)

        assert result == {"test_one:1": ["Root"]}

    def test_nested_hierarchy_builds_full_path(self):
        listener = _bare_listener()
        login = _make_suite("Login", tests=[_make_test("test_login", 5)])
        account = _make_suite("Account", suites=[login])
        login.parent = account
        root = _make_suite("Tests", suites=[account])
        account.parent = root

        result = self._extract(listener, root)

        assert result == {"test_login:5": ["Tests", "Account", "Login"]}

    def test_tests_at_multiple_levels(self):
        listener = _bare_listener()
        leaf = _make_suite("Leaf", tests=[_make_test("leaf_test", 10)])
        middle = _make_suite("Middle", suites=[leaf],
                             tests=[_make_test("mid_test", 20)])
        leaf.parent = middle
        root = _make_suite("Root", suites=[middle],
                           tests=[_make_test("root_test", 30)])
        middle.parent = root

        result = self._extract(listener, root)

        assert result == {
            "leaf_test:10": ["Root", "Middle", "Leaf"],
            "mid_test:20": ["Root", "Middle"],
            "root_test:30": ["Root"],
        }


class TestStartSuiteHierarchy:
    """Regression tests for issue #486: nested suite hierarchy is preserved."""

    def _build_tree(self):
        """Tests > Account > Login, with a single test in Login."""
        login = _make_suite("Login", tests=[_make_test("test_login", 5)])
        account = _make_suite("Account", suites=[login])
        login.parent = account
        root = _make_suite("Tests", parent=None, suites=[account])
        account.parent = root
        return root, account, login

    def _bare_listener_with_reporter(self):
        listener = _bare_listener()
        listener.reporter = MagicMock()
        listener.reporter.get_execution_plan.return_value = None
        listener.pabot_index = None
        listener.last_level_flag = None
        return listener

    def test_root_call_registers_full_hierarchy(self):
        listener = self._bare_listener_with_reporter()
        root, _, _ = self._build_tree()

        with patch("qase.robotframework.listener.get_pool_id",
                   return_value=None), \
                patch("qase.robotframework.listener.get_last_level_flag",
                      return_value=None):
            listener.start_suite(root, MagicMock())

        assert listener.tests == {
            "test_login:5": ["Tests", "Account", "Login"]
        }

    def test_child_calls_do_not_overwrite_with_shorter_path(self):
        """Robot Framework invokes start_suite for every suite in the
        hierarchy. Earlier the leaf call overwrote the full path with just
        the leaf name — that's the bug reported in #486.
        """
        listener = self._bare_listener_with_reporter()
        root, account, login = self._build_tree()

        with patch("qase.robotframework.listener.get_pool_id",
                   return_value=None), \
                patch("qase.robotframework.listener.get_last_level_flag",
                      return_value=None):
            listener.start_suite(root, MagicMock())
            listener.start_suite(account, MagicMock())
            listener.start_suite(login, MagicMock())

        assert listener.tests == {
            "test_login:5": ["Tests", "Account", "Login"]
        }

    def test_non_root_call_without_prior_root_skips_extraction(self):
        """If start_suite is invoked only for a sub-suite (e.g. when parent
        suites are filtered out), nothing is registered. This is acceptable
        because Robot Framework always emits start_suite for the run root.
        """
        listener = self._bare_listener_with_reporter()
        _, account, _ = self._build_tree()

        with patch("qase.robotframework.listener.get_pool_id",
                   return_value=None), \
                patch("qase.robotframework.listener.get_last_level_flag",
                      return_value=None):
            listener.start_suite(account, MagicMock())

        assert listener.tests == {}


class _FakeKeyword:
    """Minimal Robot Framework keyword stand-in for __parse_steps.

    The class name must be ``Keyword`` so listener's ``class_name == 'Keyword'``
    branch is taken and ``elapsed_time`` is read from the real attribute.
    """

    def __init__(self, elapsed_seconds: float):
        start = datetime(2026, 1, 1, tzinfo=timezone.utc)
        self.type = "KEYWORD"
        self.name = "Some Keyword"
        self.args = ()
        self.status = "PASS"
        self.start_time = start
        self.elapsed_time = timedelta(seconds=elapsed_seconds)
        self.end_time = start + self.elapsed_time
        self.body = []


Keyword = _FakeKeyword  # rename so __class__.__name__ == 'Keyword' inside listener


class TestParseStepsDuration:
    """Step duration must be elapsed time in milliseconds.

    Regression for the bug where duration was taking ``timedelta.microseconds``
    — the residual-microseconds field (0..999999) — instead of the full
    elapsed milliseconds, inflating sub-second durations by ~1000x.
    """

    def _parse(self, listener, body_element):
        result = MagicMock(spec=["body", "status"])
        result.body = [body_element]
        result.status = "PASS"
        return listener._Listener__parse_steps(result)

    @pytest.mark.parametrize(
        "elapsed_seconds, expected_ms",
        [
            (0.0015, 1),        # 1.5 ms → 1 ms after int()
            (0.5, 500),         # half a second → 500 ms (was 500000 before the fix)
            (2.5, 2500),        # 2.5 s → 2500 ms (was 500000: only the residual µs field)
            (12.345, 12345),    # double-digit seconds with sub-ms tail
        ],
    )
    def test_duration_is_total_elapsed_milliseconds(self, elapsed_seconds, expected_ms):
        listener = _bare_listener()
        steps = self._parse(listener, Keyword(elapsed_seconds))

        assert len(steps) == 1
        assert steps[0].execution.duration == expected_ms

    def test_start_and_end_time_round_trip(self):
        listener = _bare_listener()
        elapsed = 1.234
        keyword = Keyword(elapsed)

        steps = self._parse(listener, keyword)

        assert steps[0].execution.start_time == keyword.start_time.timestamp()
        assert steps[0].execution.end_time == keyword.end_time.timestamp()


class _FakeIfBranch:
    """Stand-in for a Robot Framework IF/ELSE branch body element."""

    def __init__(self, branch_type: str, elapsed_seconds: float, body=None):
        start = datetime(2026, 1, 1, tzinfo=timezone.utc)
        self.type = branch_type  # "IF" / "ELSE IF" / "ELSE"
        self.status = "PASS"
        self.start_time = start
        self.elapsed_time = timedelta(seconds=elapsed_seconds)
        self.end_time = start + self.elapsed_time
        self.body = body or []
        self.values = ()


class TestParseConditionStepsTiming:
    """IF/ELSE branches must carry their RF start_time/end_time/duration.

    Regression for the bug where __parse_condition_steps unconditionally
    overwrote start_time/end_time with None, so conditional branches
    showed up in TestOps without any timing data.
    """

    def _parse(self, listener, branches):
        result_step = MagicMock(spec=["body"])
        result_step.body = branches
        return listener._Listener__parse_condition_steps(result_step)

    def test_executed_if_branch_carries_real_timestamps(self):
        listener = _bare_listener()
        branch = _FakeIfBranch("IF", elapsed_seconds=0.053)

        steps = self._parse(listener, [branch])

        assert len(steps) == 1
        assert steps[0].execution.start_time == branch.start_time.timestamp()
        assert steps[0].execution.end_time == branch.end_time.timestamp()
        assert steps[0].execution.duration == 53

    def test_skipped_else_branch_still_gets_timestamps(self):
        """Skipped branches have near-zero elapsed time but must still have
        non-None start_time/end_time so the timeline shows them."""
        listener = _bare_listener()
        branch = _FakeIfBranch("ELSE", elapsed_seconds=0.0001)

        steps = self._parse(listener, [branch])

        assert steps[0].execution.start_time is not None
        assert steps[0].execution.end_time is not None
        assert steps[0].execution.duration == 0  # int(0.0001 * 1000) == 0

    def test_else_if_chain_each_branch_keeps_timing(self):
        listener = _bare_listener()
        branches = [
            _FakeIfBranch("IF", elapsed_seconds=0.0001),       # not taken
            _FakeIfBranch("ELSE IF", elapsed_seconds=0.076),   # taken
            _FakeIfBranch("ELSE", elapsed_seconds=0.0001),     # not taken
        ]

        steps = self._parse(listener, branches)

        assert [s.execution.duration for s in steps] == [0, 76, 0]
        assert all(s.execution.start_time is not None for s in steps)
        assert all(s.execution.end_time is not None for s in steps)
