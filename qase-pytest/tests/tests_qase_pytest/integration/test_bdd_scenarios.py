"""End-to-end pytest-bdd scenarios run via pytester.

Each test spins up a temporary pytest project that uses pytest-bdd and
qase-pytest in `mode=report` so we can inspect the produced JSON file
and assert the Gherkin step structure.
"""

import json

import pytest


pytest_bdd = pytest.importorskip("pytest_bdd")


REPORT_DIR_NAME = "qase_report"


def _read_results(pytester) -> list:
    """Read every result JSON file from the temporary project's report dir."""
    results_dir = pytester.path / REPORT_DIR_NAME / "results"
    if not results_dir.exists():
        return []
    out = []
    for path in sorted(results_dir.glob("*.json")):
        with open(path) as fh:
            out.append(json.load(fh))
    return out


def _write_config(pytester):
    """Write qase.config.json enabling report mode at pytester.path."""
    config = {
        "mode": "report",
        "fallback": "off",
        "debug": False,
        "report": {
            "driver": "local",
            "connection": {
                "path": str(pytester.path / REPORT_DIR_NAME),
                "format": "json",
            },
        },
    }
    (pytester.path / "qase.config.json").write_text(json.dumps(config))


def _write_feature(pytester, name, body):
    """Write a .feature file under a `features/` directory inside the project."""
    features_dir = pytester.path / "features"
    features_dir.mkdir(exist_ok=True)
    (features_dir / name).write_text(body)


def test_basic_scenario_captures_gherkin_steps(pytester):
    _write_config(pytester)
    _write_feature(
        pytester,
        "login.feature",
        """
Feature: Login
  Scenario: Successful login
    Given the user is on the login page
    When the user enters valid credentials
    Then the user should see the dashboard
""",
    )
    pytester.makepyfile(
        test_login="""
from pytest_bdd import scenarios, given, when, then

scenarios("features/login.feature")

@given("the user is on the login page")
def login_page():
    pass

@when("the user enters valid credentials")
def valid_credentials():
    pass

@then("the user should see the dashboard")
def dashboard_visible():
    pass
"""
    )

    result = pytester.runpytest_subprocess("-v")
    result.assert_outcomes(passed=1)

    results = _read_results(pytester)
    assert len(results) == 1
    r = results[0]
    assert r["title"] == "Successful login"
    assert r["execution"]["status"] == "passed"

    steps = r["steps"]
    assert len(steps) == 3
    # The report driver flattens Gherkin steps to TEXT steps when persisting
    # to JSON: keyword + name are joined into `data.action`.
    for step in steps:
        assert step["step_type"] == "text"
        assert step["execution"]["status"] == "passed"

    assert steps[0]["data"]["action"].startswith("Given")
    assert "login page" in steps[0]["data"]["action"]
    assert steps[1]["data"]["action"].startswith("When")
    assert "valid credentials" in steps[1]["data"]["action"]
    assert steps[2]["data"]["action"].startswith("Then")
    assert "dashboard" in steps[2]["data"]["action"]
