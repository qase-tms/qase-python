import pytest

from qaseio.client.models import (
    AccessLevel,
    ProjectCreate,
    Severity,
    TestCaseFilters,
    TestPlanCreate,
    TestRunCreate,
)


@pytest.mark.parametrize(
    "filters, output",
    [
        (TestCaseFilters(), {}),
        (TestCaseFilters(search="query"), {"filters[search]": "query"}),
        (TestCaseFilters(milestone_id=123), {"filters[milestone_id]": 123}),
        (
            TestCaseFilters(severity=[Severity.BLOCKER, Severity.UNDEFINED]),
            {"filters[severity]": "blocker,undefined"},
        ),
        (
            TestCaseFilters(
                search="query",
                milestone_id=123,
                severity=[Severity.BLOCKER, Severity.UNDEFINED],
            ),
            {
                "filters[search]": "query",
                "filters[milestone_id]": 123,
                "filters[severity]": "blocker,undefined",
            },
        ),
        (
            TestCaseFilters(severity=["blocker", "undefined"]),
            {"filters[severity]": "blocker,undefined"},
        ),
        (
            TestCaseFilters(severity="blocker"),
            {"filters[severity]": "blocker"},
        ),
        (TestCaseFilters(severity=[]), {}),
    ],
)
def test_filters(filters, output):
    assert filters.filter() == output


@pytest.mark.parametrize(
    "data",
    [
        ("", "TE"),
        ("a" * 65, "TESTED", "", AccessLevel.NONE),
        ("test", "TESTED", "a" * 65, AccessLevel.ALL),
        ("test", "TESTED", None, AccessLevel.GROUP, "123414"),
    ],
)
def test_valid_project_creation(data):
    ProjectCreate(*data)


@pytest.mark.parametrize(
    "data",
    [
        ("", "T"),
        ("", None),
        ("a" * 65, "TESTEDS", "", AccessLevel.NONE),
        ("test", "Tes.sd"),
        ("test", "Tes123"),
        ("test", "русский"),
        ("test", "TESTED", None, AccessLevel.GROUP),
    ],
)
def test_invalid_project_creation(data):
    with pytest.raises((ValueError, TypeError)):
        ProjectCreate(*data)


@pytest.mark.parametrize(
    "data",
    [("", [1]), ("a" * 65, [13, 14, 15], "a" * 65, 123)],
)
def test_valid_test_run_creation(data):
    TestRunCreate(*data)


@pytest.mark.parametrize(
    "data",
    [("a", []), ("a", 123)],
)
def test_invalid_test_run_creation(data):
    with pytest.raises(ValueError):
        TestRunCreate(*data)


@pytest.mark.parametrize(
    "data",
    [("", [1]), ("a" * 65, [13, 14, 15], "a" * 65)],
)
def test_valid_test_plan_creation(data):
    TestPlanCreate(*data)


@pytest.mark.parametrize(
    "data",
    [("a", []), ("a", 123)],
)
def test_invalid_test_plan_creation(data):
    with pytest.raises(ValueError):
        TestPlanCreate(*data)
