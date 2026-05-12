"""Tests for the pytest-bdd bridge plugin (QasePytestBddPlugin)."""

from unittest.mock import MagicMock

from qase.commons.models.relation import Relation, SuiteData
from qase.commons.models.result import Result


def test_bdd_module_importable():
    """The bdd module is importable and exposes QasePytestBddPlugin."""
    from qase.pytest import bdd as bdd_module

    assert hasattr(bdd_module, "QasePytestBddPlugin")


def test_bdd_plugin_constructs_with_pytest_plugin():
    """QasePytestBddPlugin can be instantiated by passing a pytest plugin instance."""
    from qase.pytest.bdd import QasePytestBddPlugin

    fake_pytest_plugin = object()
    plugin = QasePytestBddPlugin(fake_pytest_plugin)
    assert plugin is not None


def _runtime_with_result():
    """Build a Runtime-like object that exposes `.result` mutably."""
    runtime = MagicMock()
    result = Result(title="placeholder", signature="")
    rel = Relation()
    rel.add_suite(SuiteData(title="placeholder"))
    result.relations = rel
    runtime.result = result
    runtime.steps = {}
    runtime.step_id = None
    return runtime


def _fake_scenario(
    name="My Scenario",
    tags=None,
    steps=None,
    description="",
    feature_name="Feat",
    feature_desc="",
):
    feature = MagicMock()
    feature.name = feature_name
    feature.description = feature_desc
    feature.filename = "x.feature"

    scenario = MagicMock()
    scenario.name = name
    scenario.description = description
    scenario.tags = tags or set()
    scenario.steps = steps or []
    scenario.feature = feature
    # Some pytest-bdd versions expose `background` here.
    scenario.background = None
    return feature, scenario


class TestBeforeScenarioHook:
    def test_enriches_result(self):
        from qase.pytest.bdd import QasePytestBddPlugin

        pytest_plugin = MagicMock()
        pytest_plugin.runtime = _runtime_with_result()

        bdd = QasePytestBddPlugin(pytest_plugin)
        feature, scenario = _fake_scenario(
            name="Login", tags={"qase.id=42"}, feature_name="Auth"
        )

        bdd.pytest_bdd_before_scenario(
            request=MagicMock(), feature=feature, scenario=scenario
        )

        assert pytest_plugin.runtime.result.title == "Login"
        assert pytest_plugin.runtime.result.testops_ids == [42]
        suites = [s.title for s in pytest_plugin.runtime.result.relations.suite.data]
        assert suites[0] == "Auth"

    def test_caches_steps_for_skipped_finalization(self):
        from qase.pytest.bdd import QasePytestBddPlugin

        pytest_plugin = MagicMock()
        pytest_plugin.runtime = _runtime_with_result()

        bdd = QasePytestBddPlugin(pytest_plugin)
        step_a = MagicMock(
            keyword="Given", name="a", line_number=1, data_table=None, docstring=None
        )
        step_b = MagicMock(
            keyword="When", name="b", line_number=2, data_table=None, docstring=None
        )
        feature, scenario = _fake_scenario(steps=[step_a, step_b])

        bdd.pytest_bdd_before_scenario(
            request=MagicMock(), feature=feature, scenario=scenario
        )

        state = bdd._current
        assert state is not None
        assert state["remaining_steps"] == [step_a, step_b]
        assert state["next_step_idx"] == 0

    def test_no_runtime_result_is_safe(self):
        """If runtime.result is somehow None, the hook must not crash."""
        from qase.pytest.bdd import QasePytestBddPlugin

        pytest_plugin = MagicMock()
        pytest_plugin.runtime = MagicMock(result=None)

        bdd = QasePytestBddPlugin(pytest_plugin)
        feature, scenario = _fake_scenario()

        # Must not raise.
        bdd.pytest_bdd_before_scenario(
            request=MagicMock(), feature=feature, scenario=scenario
        )


class TestBeforeAfterStepHooks:
    def _setup(self):
        from qase.pytest.bdd import QasePytestBddPlugin

        pytest_plugin = MagicMock()
        runtime = _runtime_with_result()
        pytest_plugin.runtime = runtime
        bdd = QasePytestBddPlugin(pytest_plugin)
        step_a = MagicMock(
            keyword="Given", line_number=1, data_table=None, docstring=None
        )
        step_a.name = "a"
        step_b = MagicMock(
            keyword="When", line_number=2, data_table=None, docstring=None
        )
        step_b.name = "b"
        feature, scenario = _fake_scenario(steps=[step_a, step_b])
        bdd.pytest_bdd_before_scenario(
            request=MagicMock(), feature=feature, scenario=scenario
        )
        return bdd, pytest_plugin, feature, scenario, step_a, step_b

    def test_before_step_adds_step_to_runtime(self):
        bdd, pytest_plugin, feature, scenario, step_a, _ = self._setup()

        bdd.pytest_bdd_before_step(
            request=MagicMock(),
            feature=feature,
            scenario=scenario,
            step=step_a,
            step_func=MagicMock(),
        )

        # Runtime.add_step was called once with a Step(GHERKIN).
        assert pytest_plugin.runtime.add_step.call_count == 1
        added_step = pytest_plugin.runtime.add_step.call_args.args[0]
        assert added_step.data.name == "a"
        assert added_step.data.keyword == "Given"
        # ID mapping recorded.
        assert id(step_a) in bdd._current["bdd_step_to_id"]
        # Next index advanced past this step.
        assert bdd._current["next_step_idx"] == 1

    def test_after_step_marks_passed(self):
        bdd, pytest_plugin, feature, scenario, step_a, _ = self._setup()
        bdd.pytest_bdd_before_step(
            request=MagicMock(),
            feature=feature,
            scenario=scenario,
            step=step_a,
            step_func=MagicMock(),
        )

        bdd.pytest_bdd_after_step(
            request=MagicMock(),
            feature=feature,
            scenario=scenario,
            step=step_a,
            step_func=MagicMock(),
            step_func_args={"foo": "bar"},
        )

        qase_step_id = bdd._current["bdd_step_to_id"][id(step_a)]
        pytest_plugin.runtime.finish_step.assert_called_once_with(
            qase_step_id, status="passed"
        )

    def test_no_state_is_safe(self):
        """If before_scenario was never called, hooks must not crash."""
        from qase.pytest.bdd import QasePytestBddPlugin

        pytest_plugin = MagicMock()
        pytest_plugin.runtime = _runtime_with_result()
        bdd = QasePytestBddPlugin(pytest_plugin)
        step = MagicMock(
            keyword="Given", name="x", line_number=0, data_table=None, docstring=None
        )

        # Must not raise.
        bdd.pytest_bdd_before_step(
            request=MagicMock(),
            feature=MagicMock(),
            scenario=MagicMock(),
            step=step,
            step_func=MagicMock(),
        )
        bdd.pytest_bdd_after_step(
            request=MagicMock(),
            feature=MagicMock(),
            scenario=MagicMock(),
            step=step,
            step_func=MagicMock(),
            step_func_args={},
        )


class TestStepErrorAndAfterScenario:
    def _setup_two_steps(self):
        from qase.pytest.bdd import QasePytestBddPlugin

        pytest_plugin = MagicMock()
        pytest_plugin.runtime = _runtime_with_result()
        bdd = QasePytestBddPlugin(pytest_plugin)
        step_a = MagicMock(
            keyword="Given", line_number=1, data_table=None, docstring=None
        )
        step_a.name = "a"
        step_b = MagicMock(
            keyword="When", line_number=2, data_table=None, docstring=None
        )
        step_b.name = "b"
        feature, scenario = _fake_scenario(steps=[step_a, step_b])
        bdd.pytest_bdd_before_scenario(
            request=MagicMock(), feature=feature, scenario=scenario
        )
        bdd.pytest_bdd_before_step(
            request=MagicMock(),
            feature=feature,
            scenario=scenario,
            step=step_a,
            step_func=MagicMock(),
        )
        return bdd, pytest_plugin, feature, scenario, step_a, step_b

    def test_step_error_marks_failed_and_flags_scenario(self):
        bdd, pytest_plugin, feature, scenario, step_a, _ = self._setup_two_steps()

        bdd.pytest_bdd_step_error(
            request=MagicMock(),
            feature=feature,
            scenario=scenario,
            step=step_a,
            step_func=MagicMock(),
            step_func_args={},
            exception=AssertionError("boom"),
        )

        qase_id = bdd._current["bdd_step_to_id"][id(step_a)]
        pytest_plugin.runtime.finish_step.assert_called_once_with(
            qase_id, status="failed"
        )
        assert bdd._current["scenario_failed"] is True

    def test_after_scenario_skips_unreached_steps(self):
        bdd, pytest_plugin, feature, scenario, step_a, step_b = self._setup_two_steps()
        bdd.pytest_bdd_step_error(
            request=MagicMock(),
            feature=feature,
            scenario=scenario,
            step=step_a,
            step_func=MagicMock(),
            step_func_args={},
            exception=AssertionError("boom"),
        )

        bdd.pytest_bdd_after_scenario(
            request=MagicMock(), feature=feature, scenario=scenario
        )

        # step_b was never started; must be added directly with status='skipped'.
        added = pytest_plugin.runtime.steps
        skipped_steps = [s for s in added.values() if s.execution.status == "skipped"]
        assert len(skipped_steps) == 1
        assert skipped_steps[0].data.name == "b"

    def test_after_scenario_clears_state(self):
        bdd, pytest_plugin, feature, scenario, *_ = self._setup_two_steps()
        bdd.pytest_bdd_after_scenario(
            request=MagicMock(), feature=feature, scenario=scenario
        )
        assert bdd._current is None

    def test_after_scenario_no_skipped_when_all_passed(self):
        bdd, pytest_plugin, feature, scenario, step_a, step_b = self._setup_two_steps()
        # Run step_a all the way, then step_b all the way.
        bdd.pytest_bdd_after_step(
            request=MagicMock(),
            feature=feature,
            scenario=scenario,
            step=step_a,
            step_func=MagicMock(),
            step_func_args={},
        )
        bdd.pytest_bdd_before_step(
            request=MagicMock(),
            feature=feature,
            scenario=scenario,
            step=step_b,
            step_func=MagicMock(),
        )
        bdd.pytest_bdd_after_step(
            request=MagicMock(),
            feature=feature,
            scenario=scenario,
            step=step_b,
            step_func=MagicMock(),
            step_func_args={},
        )

        bdd.pytest_bdd_after_scenario(
            request=MagicMock(), feature=feature, scenario=scenario
        )

        # No "skipped" steps should appear when all steps ran.
        added = pytest_plugin.runtime.steps
        skipped = [s for s in added.values() if s.execution.status == "skipped"]
        assert skipped == []


class TestStepLookupError:
    def test_lookup_error_records_invalid_step(self):
        from qase.pytest.bdd import QasePytestBddPlugin

        pytest_plugin = MagicMock()
        pytest_plugin.runtime = _runtime_with_result()
        bdd = QasePytestBddPlugin(pytest_plugin)
        step = MagicMock(
            keyword="Given", line_number=3, data_table=None, docstring=None
        )
        step.name = "missing impl"
        feature, scenario = _fake_scenario(steps=[step])
        bdd.pytest_bdd_before_scenario(
            request=MagicMock(), feature=feature, scenario=scenario
        )

        bdd.pytest_bdd_step_func_lookup_error(
            request=MagicMock(),
            feature=feature,
            scenario=scenario,
            step=step,
            exception=Exception("no def for step"),
        )

        added = pytest_plugin.runtime.steps
        invalid = [s for s in added.values() if s.execution.status == "invalid"]
        assert len(invalid) == 1
        assert invalid[0].data.name == "missing impl"
        assert bdd._current["scenario_failed"] is True
