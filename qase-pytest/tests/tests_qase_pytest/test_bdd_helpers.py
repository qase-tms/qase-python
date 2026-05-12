"""Unit tests for pure helpers in qase.pytest.bdd."""

from qase.commons.models.relation import Relation, SuiteData
from qase.commons.models.result import Result
from qase.commons.models.step import StepType

from qase.pytest.bdd import (
    build_step,
    enrich_result_from_scenario,
    format_data_table,
    format_docstring,
    parse_scenario_tags,
)


class _FakeCell:
    def __init__(self, value):
        self.value = value


class _FakeRow:
    def __init__(self, values):
        self.cells = [_FakeCell(v) for v in values]


class _FakeDataTable:
    def __init__(self, rows):
        self.rows = [_FakeRow(r) for r in rows]


class TestParseScenarioTags:
    def test_empty_returns_empty_dict(self):
        result = parse_scenario_tags([])
        assert result["testops_ids"] is None
        assert result["testops_project_mapping"] is None
        assert result["ignore"] is False
        assert result["muted"] is False
        assert result["suite"] is None
        assert result["fields"] == {}
        assert result["tags"] == []

    def test_qase_id_single(self):
        result = parse_scenario_tags(["qase.id=42"])
        assert result["testops_ids"] == [42]

    def test_qase_id_multiple(self):
        result = parse_scenario_tags(["qase.id=42,43,44"])
        assert result["testops_ids"] == [42, 43, 44]

    def test_qase_id_multiple_with_spaces(self):
        result = parse_scenario_tags(["qase.id=42, 43 ,44"])
        assert result["testops_ids"] == [42, 43, 44]

    def test_repeated_qase_id_keeps_last(self):
        # Duplicated tags are user error in the .feature file, but the parser
        # behaves deterministically: the last one wins. Lock that contract.
        result = parse_scenario_tags(["qase.id=42", "qase.id=99"])
        assert result["testops_ids"] == [99]

    def test_qase_project_id_multi_project(self):
        result = parse_scenario_tags(
            [
                "qase.project_id.PROJ_A=1,2",
                "qase.project_id.PROJ_B=3",
            ]
        )
        assert result["testops_project_mapping"] == {
            "PROJ_A": [1, 2],
            "PROJ_B": [3],
        }

    def test_qase_project_id_with_dotted_code_is_accepted(self):
        # Mirrors qase-behave parser: extra dots inside the project code are
        # passed through verbatim. This is intentional consistency.
        result = parse_scenario_tags(["qase.project_id.A.B=1"])
        assert result["testops_project_mapping"] == {"A.B": [1]}

    def test_ignore_flag(self):
        result = parse_scenario_tags(["qase.ignore"])
        assert result["ignore"] is True

    def test_muted_flag(self):
        result = parse_scenario_tags(["qase.muted"])
        assert result["muted"] is True

    def test_suite_simple(self):
        result = parse_scenario_tags(["qase.suite=Login"])
        assert result["suite"] == ["Login"]

    def test_suite_nested_dot_notation(self):
        result = parse_scenario_tags(["qase.suite=Login.Smoke.Critical"])
        assert result["suite"] == ["Login", "Smoke", "Critical"]

    def test_known_fields(self):
        result = parse_scenario_tags(
            [
                "qase.severity=critical",
                "qase.priority=high",
                "qase.layer=e2e",
            ]
        )
        assert result["fields"] == {
            "severity": "critical",
            "priority": "high",
            "layer": "e2e",
        }

    def test_free_tags_passthrough(self):
        result = parse_scenario_tags(["smoke", "regression"])
        assert result["tags"] == ["smoke", "regression"]

    def test_at_prefix_is_stripped(self):
        # pytest-bdd usually exposes tags without "@", but be defensive.
        result = parse_scenario_tags(["@qase.id=99", "@smoke"])
        assert result["testops_ids"] == [99]
        assert result["tags"] == ["smoke"]

    def test_unknown_qase_tag_falls_through_to_tags(self):
        # qase.foo is not recognized; treat as a free tag, not silent loss.
        result = parse_scenario_tags(["qase.unknown=bar"])
        assert "qase.unknown=bar" in result["tags"]

    def test_invalid_id_value_is_ignored(self):
        # Non-int values must not crash the parser.
        result = parse_scenario_tags(["qase.id=abc"])
        assert result["testops_ids"] is None


class TestFormatDataTable:
    def test_none_returns_empty_string(self):
        assert format_data_table(None) == ""

    def test_simple_table(self):
        table = _FakeDataTable(
            [
                ["name", "email"],
                ["Alice", "alice@example.com"],
                ["Bob", "bob@example.com"],
            ]
        )
        result = format_data_table(table)
        assert result == (
            "| name | email |\n"
            "| --- | --- |\n"
            "| Alice | alice@example.com |\n"
            "| Bob | bob@example.com |"
        )

    def test_single_row_header_only(self):
        table = _FakeDataTable([["col1", "col2"]])
        result = format_data_table(table)
        assert result == "| col1 | col2 |\n| --- | --- |"

    def test_empty_table_returns_empty_string(self):
        table = _FakeDataTable([])
        assert format_data_table(table) == ""

    def test_escapes_pipes_in_values(self):
        table = _FakeDataTable([["a", "b"], ["x|y", "z"]])
        result = format_data_table(table)
        assert "x\\|y" in result

    def test_escapes_backslashes_before_pipes(self):
        table = _FakeDataTable([["a"], ["C:\\Users"]])
        result = format_data_table(table)
        # Backslash must be escaped as \\, not left bare.
        assert "C:\\\\Users" in result

    def test_replaces_newlines_with_br_inside_cells(self):
        table = _FakeDataTable([["a"], ["line1\nline2"]])
        result = format_data_table(table)
        # Newline must not split the row; rendered as <br>.
        assert "line1<br>line2" in result
        # The cell stays on a single output line.
        assert "line1\nline2" not in result


class TestFormatDocstring:
    def test_none_returns_empty_string(self):
        assert format_docstring(None) == ""

    def test_empty_string_returns_empty_string(self):
        assert format_docstring("") == ""

    def test_single_line(self):
        assert format_docstring("hello") == "```\nhello\n```"

    def test_multiline_preserved(self):
        text = "line1\nline2\nline3"
        assert format_docstring(text) == "```\nline1\nline2\nline3\n```"

    def test_strips_only_outer_blank_lines(self):
        # pytest-bdd sometimes includes leading/trailing blank lines from
        # triple-quote indentation.
        text = "\n\nline\n\n"
        assert format_docstring(text) == "```\nline\n```"

    def test_whitespace_only_returns_empty_string(self):
        # Whitespace-only input collapses to empty after stripping.
        assert format_docstring("\n\n  \n") == ""

    def test_triple_backticks_inside_uses_longer_fence(self):
        text = "before\n```\ninner\n```\nafter"
        result = format_docstring(text)
        # Fence must be 4+ backticks to safely wrap content with a `` ``` `` run.
        assert result.startswith("````\n")
        assert result.endswith("\n````")
        # The original triple-backtick content is preserved unchanged.
        assert "```\ninner\n```" in result


class _FakeBddStep:
    def __init__(
        self,
        keyword="Given",
        name="something happens",
        line_number=3,
        data_table=None,
        docstring=None,
    ):
        self.keyword = keyword
        self.name = name
        self.line_number = line_number
        self.data_table = data_table
        self.docstring = docstring


class TestBuildStep:
    def test_basic_step(self):
        step = build_step(_FakeBddStep("Given", "a user", 5))
        assert step.step_type == StepType.GHERKIN
        assert step.data.keyword == "Given"
        assert step.data.name == "a user"
        assert step.data.line == 5
        assert step.data.data is None

    def test_when_keyword(self):
        step = build_step(_FakeBddStep("When", "they click", 7))
        assert step.data.keyword == "When"

    def test_with_data_table(self):
        # _FakeDataTable is defined module-level in this test file
        # (see TestFormatDataTable section above).
        table = _FakeDataTable([["a", "b"], ["1", "2"]])
        step = build_step(_FakeBddStep("Given", "table", 5, data_table=table))
        assert "| a | b |" in step.data.data
        assert "| 1 | 2 |" in step.data.data

    def test_with_docstring(self):
        step = build_step(_FakeBddStep("When", "send body", 5, docstring="payload"))
        # Default fence is 3 backticks because there are no backticks in "payload".
        assert step.data.data == "```\npayload\n```"

    def test_default_line_when_missing(self):
        s = _FakeBddStep("Given", "x", 0)
        del s.line_number  # simulate missing attribute on older pytest-bdd
        step = build_step(s)
        assert step.data.line == 0

    def test_each_call_returns_unique_id(self):
        s1 = build_step(_FakeBddStep())
        s2 = build_step(_FakeBddStep())
        assert s1.id != s2.id


class _FakeFeature:
    def __init__(
        self,
        name="My Feature",
        description="Feature desc",
        filename="features/x.feature",
    ):
        self.name = name
        self.description = description
        self.filename = filename


class _FakeScenario:
    def __init__(
        self,
        name="My Scenario",
        description="",
        tags=None,
        feature=None,
    ):
        self.name = name
        self.description = description
        self.tags = tags or set()
        self.feature = feature or _FakeFeature()


class TestEnrichResultFromScenario:
    def _new_result(self):
        r = Result(title="placeholder", signature="")
        rel = Relation()
        rel.add_suite(SuiteData(title="placeholder_suite"))
        r.relations = rel
        return r

    def test_title_replaced_by_scenario_name(self):
        r = self._new_result()
        enrich_result_from_scenario(r, _FakeFeature(), _FakeScenario(name="Login OK"))
        assert r.title == "Login OK"

    def test_feature_prepended_to_suite_chain(self):
        r = self._new_result()
        feature = _FakeFeature(name="Auth")
        enrich_result_from_scenario(r, feature, _FakeScenario())
        suites = [s.title for s in r.relations.suite.data]
        assert suites[0] == "Auth"

    def test_description_combines_feature_and_scenario(self):
        r = self._new_result()
        feature = _FakeFeature(description="Big feature description")
        scenario = _FakeScenario(description="Specific scenario context")
        enrich_result_from_scenario(r, feature, scenario)
        assert "Big feature description" in r.fields["description"]
        assert "Specific scenario context" in r.fields["description"]

    def test_only_feature_description(self):
        r = self._new_result()
        feature = _FakeFeature(description="Just feature")
        scenario = _FakeScenario(description="")
        enrich_result_from_scenario(r, feature, scenario)
        assert r.fields["description"].strip() == "Just feature"

    def test_no_description_field_when_both_empty(self):
        r = self._new_result()
        feature = _FakeFeature(description="")
        scenario = _FakeScenario(description="")
        enrich_result_from_scenario(r, feature, scenario)
        assert "description" not in r.fields

    def test_testops_ids_from_tag(self):
        r = self._new_result()
        enrich_result_from_scenario(
            r, _FakeFeature(), _FakeScenario(tags={"qase.id=42"})
        )
        assert r.testops_ids == [42]

    def test_suite_override_replaces_chain(self):
        r = self._new_result()
        enrich_result_from_scenario(
            r,
            _FakeFeature(name="ShouldBeIgnored"),
            _FakeScenario(tags={"qase.suite=Login.Smoke"}),
        )
        suites = [s.title for s in r.relations.suite.data]
        assert suites == ["Login", "Smoke"]

    def test_severity_priority_layer_fields(self):
        r = self._new_result()
        enrich_result_from_scenario(
            r,
            _FakeFeature(),
            _FakeScenario(
                tags={
                    "qase.severity=critical",
                    "qase.priority=high",
                    "qase.layer=e2e",
                }
            ),
        )
        assert r.fields["severity"] == "critical"
        assert r.fields["priority"] == "high"
        assert r.fields["layer"] == "e2e"

    def test_muted_flag(self):
        r = self._new_result()
        enrich_result_from_scenario(
            r, _FakeFeature(), _FakeScenario(tags={"qase.muted"})
        )
        assert r.muted is True

    def test_ignore_flag(self):
        r = self._new_result()
        enrich_result_from_scenario(
            r, _FakeFeature(), _FakeScenario(tags={"qase.ignore"})
        )
        assert getattr(r, "ignore", False) is True

    def test_free_tags_added_to_result(self):
        r = self._new_result()
        enrich_result_from_scenario(
            r,
            _FakeFeature(),
            _FakeScenario(tags={"smoke", "regression"}),
        )
        assert "smoke" in r.tags
        assert "regression" in r.tags

    def test_project_id_mapping(self):
        r = self._new_result()
        enrich_result_from_scenario(
            r,
            _FakeFeature(),
            _FakeScenario(
                tags={"qase.project_id.PROJ_A=1,2", "qase.project_id.PROJ_B=3"}
            ),
        )
        assert r.get_testops_ids_for_project("PROJ_A") == [1, 2]
        assert r.get_testops_ids_for_project("PROJ_B") == [3]
