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
    pytester.makepyfile(test_login="""
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
""")

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


def test_failing_step_skips_remaining(pytester):
    _write_config(pytester)
    _write_feature(
        pytester,
        "math.feature",
        """
Feature: Math
  Scenario: Bad math
    Given a calculator
    When I add 2 and 2
    Then the result is 5
""",
    )
    pytester.makepyfile(test_math="""
from pytest_bdd import scenarios, given, when, then

scenarios("features/math.feature")

@given("a calculator")
def a_calc():
    pass

@when("I add 2 and 2")
def add():
    pass

@then("the result is 5")
def assert_five():
    assert 2 + 2 == 5
""")

    result = pytester.runpytest_subprocess("-v")
    result.assert_outcomes(failed=1)

    results = _read_results(pytester)
    assert len(results) == 1
    steps = results[0]["steps"]
    assert len(steps) == 3
    assert steps[0]["execution"]["status"] == "passed"
    assert steps[1]["execution"]["status"] == "passed"
    assert steps[2]["execution"]["status"] == "failed"


def test_assert_in_first_step_skips_rest(pytester):
    _write_config(pytester)
    _write_feature(
        pytester,
        "fail_first.feature",
        """
Feature: Fail early
  Scenario: Boom
    Given an impossible precondition
    When something happens
    Then we observe an outcome
""",
    )
    pytester.makepyfile(test_fail="""
from pytest_bdd import scenarios, given, when, then

scenarios("features/fail_first.feature")

@given("an impossible precondition")
def precond():
    assert False, "nope"

@when("something happens")
def happens():
    pass

@then("we observe an outcome")
def outcome():
    pass
""")

    result = pytester.runpytest_subprocess("-v")
    result.assert_outcomes(failed=1)

    results = _read_results(pytester)
    steps = results[0]["steps"]
    statuses = [s["execution"]["status"] for s in steps]
    assert statuses[0] == "failed"
    assert statuses[1] == "skipped"
    assert statuses[2] == "skipped"


def test_step_lookup_error_marks_step_invalid(pytester):
    _write_config(pytester)
    _write_feature(
        pytester,
        "missing.feature",
        """
Feature: Missing impl
  Scenario: Step not implemented
    Given a step that has an implementation
    When a step that nobody has implemented
""",
    )
    pytester.makepyfile(test_missing="""
from pytest_bdd import scenarios, given

scenarios("features/missing.feature")

@given("a step that has an implementation")
def implemented():
    pass
""")

    pytester.runpytest_subprocess("-v")

    results = _read_results(pytester)
    assert len(results) == 1
    steps = results[0]["steps"]
    statuses = [s["execution"]["status"] for s in steps]
    # First step passes (it has an implementation).
    assert statuses[0] == "passed"
    # The missing one should be marked invalid by our plugin.
    assert "invalid" in statuses


def test_nested_qase_step_inherits_gherkin_parent(pytester):
    _write_config(pytester)
    _write_feature(
        pytester,
        "nested.feature",
        """
Feature: Nested
  Scenario: User flow
    Given the user opens the page
""",
    )
    pytester.makepyfile(test_nested="""
from pytest_bdd import scenarios, given
from qase.pytest import qase

scenarios("features/nested.feature")

@given("the user opens the page")
def opens():
    with qase.step("Navigate"):
        pass
    with qase.step("Wait for load"):
        pass
""")

    result = pytester.runpytest_subprocess("-v")
    result.assert_outcomes(passed=1)

    results = _read_results(pytester)
    steps = results[0]["steps"]
    # One top-level Gherkin step (flattened to text in the report) with two children.
    assert len(steps) == 1
    assert len(steps[0]["steps"]) == 2
    # Child step actions are the qase.step() titles.
    child_actions = {child["data"]["action"] for child in steps[0]["steps"]}
    assert child_actions == {"Navigate", "Wait for load"}


def test_scenario_outline_produces_multiple_parameterized_results(pytester):
    _write_config(pytester)
    _write_feature(
        pytester,
        "outline.feature",
        """
Feature: Outline
  Scenario Outline: Adding numbers
    Given I have <a> and <b>
    Then their sum is <c>

    Examples:
      | a | b | c  |
      | 1 | 2 | 3  |
      | 5 | 7 | 12 |
""",
    )
    pytester.makepyfile(test_outline="""
from pytest_bdd import scenarios, given, then, parsers

scenarios("features/outline.feature")

@given(parsers.parse("I have {a:d} and {b:d}"), target_fixture="numbers")
def numbers(a, b):
    return a, b

@then(parsers.parse("their sum is {c:d}"))
def check_sum(numbers, c):
    assert sum(numbers) == c
""")

    result = pytester.runpytest_subprocess("-v")
    result.assert_outcomes(passed=2)

    results = _read_results(pytester)
    assert len(results) == 2
    # Each result should have its own params populated (from pytest-bdd's
    # Examples-to-parametrize conversion captured by the existing _set_params).
    all_params = [r.get("params") or {} for r in results]
    # Each result must have the Examples row exploded into individual params,
    # not a single ugly _pytest_bdd_example key.
    all_keys = set()
    for p in all_params:
        assert (
            "_pytest_bdd_example" not in p
        ), "Scenario Outline params should be exploded, not kept as a single key"
        all_keys.update(p.keys())
    assert {"a", "b", "c"}.issubset(
        all_keys
    ), f"expected a/b/c in exploded params, got keys: {sorted(all_keys)}"


def test_data_table_and_docstring_preserved(pytester):
    _write_config(pytester)
    _write_feature(
        pytester,
        "data.feature",
        '''
Feature: Data carriers
  Scenario: With table and docstring
    Given the following users:
      | name  | role  |
      | Alice | admin |
      | Bob   | user  |
    When I send the payload:
      """
      {"key": "value"}
      """
''',
    )
    pytester.makepyfile(test_data="""
from pytest_bdd import scenarios, given, when

scenarios("features/data.feature")

@given("the following users:")
def users():
    pass

@when("I send the payload:")
def payload():
    pass
""")

    pytester.runpytest_subprocess("-v")
    results = _read_results(pytester)
    assert len(results) == 1
    steps = results[0]["steps"]
    assert len(steps) == 2
    # DataTable formatted as markdown by format_data_table() lands in input_data.
    table_payload = steps[0]["data"]["input_data"] or ""
    assert "| name | role |" in table_payload
    # The DocString is wrapped as a fenced code block by format_docstring().
    docstring_payload = steps[1]["data"]["input_data"] or ""
    assert docstring_payload.startswith("```")
    assert '"key": "value"' in docstring_payload


def test_scenario_tags_map_to_qase_fields(pytester):
    _write_config(pytester)
    _write_feature(
        pytester,
        "tagged.feature",
        """
Feature: Tagged
  @qase.id=42 @qase.suite=Login.Smoke @qase.severity=critical @smoke
  Scenario: Tagged scenario
    Given a step
""",
    )
    pytester.makepyfile(test_tagged="""
from pytest_bdd import scenarios, given

scenarios("features/tagged.feature")

@given("a step")
def step_impl():
    pass
""")

    pytester.runpytest_subprocess("-v")
    results = _read_results(pytester)
    assert len(results) == 1
    r = results[0]
    assert r["testops_ids"] == [42]
    suites = [s["title"] for s in r["relations"]["suite"]["data"]]
    assert suites == ["Login", "Smoke"]
    assert r["fields"]["severity"] == "critical"
    assert "smoke" in r["tags"]


def test_scenario_with_qase_ignore_is_skipped(pytester):
    _write_config(pytester)
    _write_feature(
        pytester,
        "ignored.feature",
        """
Feature: Ignored
  @qase.ignore
  Scenario: Should not be reported
    Given a step
""",
    )
    pytester.makepyfile(test_ignored="""
from pytest_bdd import scenarios, given

scenarios("features/ignored.feature")

@given("a step")
def step_impl():
    pass
""")

    pytester.runpytest_subprocess("-v")
    results = _read_results(pytester)
    # The scenario is marked @qase.ignore — it must not appear in the report.
    assert results == []


def test_bdd_and_plain_pytest_coexist(pytester):
    _write_config(pytester)
    _write_feature(
        pytester,
        "coexist.feature",
        """
Feature: Coexist
  Scenario: BDD path
    Given a bdd step
""",
    )
    pytester.makepyfile(
        test_bdd="""
from pytest_bdd import scenarios, given

scenarios("features/coexist.feature")

@given("a bdd step")
def bdd_step():
    pass
""",
        test_plain="""
def test_plain_passes():
    assert 1 + 1 == 2
""",
    )

    result = pytester.runpytest_subprocess("-v")
    result.assert_outcomes(passed=2)

    results = _read_results(pytester)
    assert len(results) == 2
    titles = {r["title"] for r in results}
    # The BDD test should expose its scenario name as title; the plain test
    # keeps its function name.
    assert "BDD path" in titles
    assert "test_plain_passes" in titles
