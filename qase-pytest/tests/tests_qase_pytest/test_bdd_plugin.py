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
