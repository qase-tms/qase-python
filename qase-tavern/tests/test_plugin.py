"""Tests for Tavern QasePytestPlugin error scenarios and edge cases.

Supplements test_extractor.py (happy path) with error paths, multi-project
handling, and edge cases for _get_title, _set_relations, and _set_steps.
"""

from unittest.mock import MagicMock, patch

import pytest

from qase.commons.models import Result
from qase.tavern.plugin import QasePytestPlugin, QasePytestPluginSingleton


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(autouse=True)
def _reset_singleton():
    """Ensure singleton is reset after each test."""
    yield
    QasePytestPluginSingleton._instance = None


def _make_plugin(with_result=False):
    """Create a QasePytestPlugin with a mock reporter.

    Args:
        with_result: If True, initialise runtime.result so that instance
            methods like _set_relations and _set_steps can access it.
    """
    reporter = MagicMock()
    reporter.config = MagicMock()
    plugin = QasePytestPlugin(reporter=reporter)
    if with_result:
        plugin.runtime.result = Result(title="test", signature="test")
    return plugin


# ---------------------------------------------------------------------------
# extract_qase_ids -- error paths
# ---------------------------------------------------------------------------


class TestExtractQaseIdsErrors:
    """Error paths for extract_qase_ids (non-string inputs)."""

    def test_int_input_raises_value_error(self):
        with pytest.raises(ValueError, match="Expected a string"):
            QasePytestPlugin.extract_qase_ids(123)

    def test_none_input_raises_value_error(self):
        with pytest.raises(ValueError, match="Expected a string"):
            QasePytestPlugin.extract_qase_ids(None)

    def test_list_input_raises_value_error(self):
        with pytest.raises(ValueError, match="Expected a string"):
            QasePytestPlugin.extract_qase_ids([1, 2])

    def test_empty_string_returns_empty(self):
        qase_ids, project_ids, remaining, tags = QasePytestPlugin.extract_qase_ids("")
        assert qase_ids == []
        assert project_ids == {}
        assert remaining == ""
        assert tags == []

    def test_no_matching_pattern_returns_original_text(self):
        text = "No IDs here"
        qase_ids, project_ids, remaining, tags = QasePytestPlugin.extract_qase_ids(text)
        assert qase_ids == []
        assert project_ids == {}
        assert remaining == "No IDs here"
        assert tags == []


# ---------------------------------------------------------------------------
# extract_qase_ids -- multi-project
# ---------------------------------------------------------------------------


class TestExtractQaseIdsMultiProject:
    """Multi-project ID extraction tests."""

    def test_multiple_project_ids(self):
        text = "QaseProjectID.PROJ1=1,2 QaseProjectID.PROJ2=3"
        qase_ids, project_ids, remaining, tags = QasePytestPlugin.extract_qase_ids(text)
        assert qase_ids == []
        assert project_ids == {"PROJ1": [1, 2], "PROJ2": [3]}
        assert tags == []

    def test_project_ids_take_precedence_over_qase_ids(self):
        """When both QaseProjectID and QaseID present, qase_ids stays empty."""
        text = "QaseProjectID.PROJ1=10 QaseID=99"
        qase_ids, project_ids, remaining, tags = QasePytestPlugin.extract_qase_ids(text)
        assert qase_ids == []
        assert project_ids == {"PROJ1": [10]}
        assert tags == []

    def test_single_project_multiple_ids(self):
        text = "QaseProjectID.MYPROJ=100,200,300"
        qase_ids, project_ids, remaining, tags = QasePytestPlugin.extract_qase_ids(text)
        assert project_ids == {"MYPROJ": [100, 200, 300]}
        assert qase_ids == []
        assert tags == []


# ---------------------------------------------------------------------------
# _get_title -- static method
# ---------------------------------------------------------------------------


class TestGetTitle:
    """Tests for _get_title static method."""

    def test_item_with_spec_returns_test_name(self):
        item = MagicMock()
        item.spec = {"test_name": "my_test_case"}
        assert QasePytestPlugin._get_title(item) == "my_test_case"

    def test_item_without_spec_returns_empty_string(self):
        item = MagicMock(spec=[])  # MagicMock spec=[] makes hasattr(item, "spec") False
        del item.spec
        assert QasePytestPlugin._get_title(item) == ""


# ---------------------------------------------------------------------------
# _set_relations -- instance method
# ---------------------------------------------------------------------------


class TestSetRelations:
    """Tests for _set_relations with missing fspath."""

    def test_item_with_fspath_creates_relation(self):
        plugin = _make_plugin(with_result=True)
        item = MagicMock()
        item.fspath.basename = "test_suite.yaml"
        plugin._set_relations(item)
        assert plugin.runtime.result.relations is not None

    def test_item_without_fspath_no_crash(self):
        """Item without fspath attribute should not crash."""
        plugin = _make_plugin(with_result=True)
        item = MagicMock(spec=[])
        del item.fspath
        # Should not raise
        plugin._set_relations(item)

    def test_item_fspath_without_basename_no_crash(self):
        """Item with fspath but no basename should not crash."""
        plugin = _make_plugin(with_result=True)
        item = MagicMock()
        del item.fspath.basename
        # Should not raise
        plugin._set_relations(item)


# ---------------------------------------------------------------------------
# _set_steps -- instance method
# ---------------------------------------------------------------------------


class TestSetSteps:
    """Tests for _set_steps edge cases."""

    def test_item_without_spec_no_crash(self):
        """Item without spec attribute should not crash."""
        plugin = _make_plugin(with_result=True)
        item = MagicMock(spec=[])
        del item.spec
        # Should not raise
        plugin._set_steps(item)

    def test_item_with_spec_iterates_stages(self):
        """Item with spec and stages should iterate through stages.

        NOTE: The actual __prepare_step accesses step.attachments which
        doesn't exist on the Step model (it lives on step.execution).
        This is a pre-existing issue in the plugin. Here we verify _set_steps
        at least enters the loop by checking the call count on add_step.
        """
        plugin = _make_plugin(with_result=True)
        plugin.runtime = MagicMock()
        item = MagicMock()
        item.spec = {
            "stages": [
                {
                    "name": "Login request",
                    "request": {"url": "/api/login", "method": "POST"},
                    "response": {"status_code": 200},
                },
            ]
        }
        # __prepare_step is private, so we need to patch the step creation
        # to avoid the attachments AttributeError
        with patch.object(
            QasePytestPlugin,
            "_QasePytestPlugin__prepare_step",
            return_value=MagicMock(),
        ):
            plugin._set_steps(item)
        plugin.runtime.add_step.assert_called_once()


# ---------------------------------------------------------------------------
# extract_qase_ids -- tags extraction
# ---------------------------------------------------------------------------


class TestExtractQaseIdsTags:
    """Tags extraction from test names."""

    def test_single_tag(self):
        qase_ids, project_ids, remaining, tags = QasePytestPlugin.extract_qase_ids(
            "QaseID=101 QaseTags.smoke Get users"
        )
        assert qase_ids == [101]
        assert tags == ["smoke"]
        assert remaining == "Get users"

    def test_multiple_tags(self):
        qase_ids, project_ids, remaining, tags = QasePytestPlugin.extract_qase_ids(
            "QaseID=102 QaseTags.smoke,regression,api Get users"
        )
        assert tags == ["smoke", "regression", "api"]

    def test_tags_without_qase_id(self):
        qase_ids, project_ids, remaining, tags = QasePytestPlugin.extract_qase_ids(
            "QaseTags.smoke Simple test"
        )
        assert qase_ids == []
        assert tags == ["smoke"]
        assert remaining == "Simple test"

    def test_no_tags_returns_empty_list(self):
        qase_ids, project_ids, remaining, tags = QasePytestPlugin.extract_qase_ids(
            "QaseID=101 Get users"
        )
        assert tags == []

    def test_tags_case_insensitive(self):
        qase_ids, project_ids, remaining, tags = QasePytestPlugin.extract_qase_ids(
            "qasetags.smoke Test"
        )
        assert tags == ["smoke"]


# ---------------------------------------------------------------------------
# pytest_tavern_beta_* hooks -- per-stage timing
# ---------------------------------------------------------------------------


class TestTavernBetaHooksTiming:
    """Each Tavern stage must carry its own start_time/end_time.

    Regression for the bug where all Step() objects were created up-front
    in start_pytest_item (so they shared one start_time), and then closed
    in a single makereport loop (so they shared one end_time), making the
    TestOps timeline collapse all stages onto the same instant.
    """

    def _plugin_with_steps(self, stages):
        """Create a plugin with one Step per stage and a fresh stage index."""
        plugin = _make_plugin(with_result=True)
        from qase.commons.models.step import Step, StepType, StepTextData

        for name in stages:
            step = Step(StepType.TEXT, name, StepTextData(name))
            plugin.runtime.add_step(step)
        plugin._tavern_stage_index = 0
        return plugin

    def test_each_stage_gets_distinct_timings(self):
        plugin = self._plugin_with_steps(["s1", "s2", "s3"])

        plugin.pytest_tavern_beta_before_every_request(request_args={})
        plugin.pytest_tavern_beta_after_every_response(expected={}, response=None)

        plugin.pytest_tavern_beta_before_every_request(request_args={})
        plugin.pytest_tavern_beta_after_every_response(expected={}, response=None)

        plugin.pytest_tavern_beta_before_every_request(request_args={})
        plugin.pytest_tavern_beta_after_every_response(expected={}, response=None)

        starts = [s.execution.start_time for s in plugin.runtime.steps.values()]
        ends = [s.execution.end_time for s in plugin.runtime.steps.values()]

        # Hooks fire in real time, so each start must be >= the previous end.
        assert starts[0] < ends[0] <= starts[1] < ends[1] <= starts[2] < ends[2]
        # And no two steps share the same start/end.
        assert len(set(starts)) == 3
        assert len(set(ends)) == 3

    def test_hooks_advance_only_one_stage_per_pair(self):
        plugin = self._plugin_with_steps(["s1", "s2"])

        plugin.pytest_tavern_beta_before_every_request(request_args={})
        plugin.pytest_tavern_beta_after_every_response(expected={}, response=None)

        assert plugin._tavern_stage_index == 1
        # s2 must still be untouched by hooks.
        s2 = list(plugin.runtime.steps.values())[1]
        # complete() sets end_time to float; un-completed default is 0.
        assert s2.execution.end_time == 0

    def test_extra_hook_calls_after_last_stage_are_ignored(self):
        """If Tavern fires more hooks than we have steps (e.g. MQTT multiple
        responses) we must not crash or wrap around to the first step."""
        plugin = self._plugin_with_steps(["only"])

        plugin.pytest_tavern_beta_before_every_request(request_args={})
        plugin.pytest_tavern_beta_after_every_response(expected={}, response=None)

        original_end = list(plugin.runtime.steps.values())[0].execution.end_time

        # One extra spurious pair — must not touch the existing step.
        plugin.pytest_tavern_beta_before_every_request(request_args={})
        plugin.pytest_tavern_beta_after_every_response(expected={}, response=None)

        assert list(plugin.runtime.steps.values())[0].execution.end_time == original_end

    def test_ensure_step_closed_skips_already_closed(self):
        plugin = _make_plugin(with_result=True)
        from qase.commons.models.step import Step, StepType, StepTextData

        step = Step(StepType.TEXT, "s", StepTextData("s"))
        step.execution.start_time = 100.0
        step.execution.end_time = 100.5
        step.execution.duration = 500

        plugin._ensure_step_closed(step, "passed")

        # Original timings preserved; only status updated.
        assert step.execution.start_time == 100.0
        assert step.execution.end_time == 100.5
        assert step.execution.duration == 500
        assert step.execution.status == "passed"

    def test_ensure_step_closed_marks_unrun_skipped_as_zero_duration(self):
        plugin = _make_plugin(with_result=True)
        from qase.commons.models.step import Step, StepType, StepTextData

        step = Step(StepType.TEXT, "s", StepTextData("s"))
        original_start = step.execution.start_time  # set by StepExecution.__init__

        plugin._ensure_step_closed(step, "skipped")

        # Step never ran — give it a zero-duration placeholder at "now",
        # not a duration spanning the whole test.
        assert step.execution.start_time != original_start
        assert step.execution.start_time == step.execution.end_time
        assert step.execution.duration == 0
        assert step.execution.status == "skipped"
