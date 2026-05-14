"""Tests for Listener static helper methods.

Only tests static/class methods that do NOT require Robot Framework runtime
or ConfigManager/QaseCoreReporter initialization.
"""

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
