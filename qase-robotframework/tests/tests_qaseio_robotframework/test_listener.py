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
