"""Unit tests for pure helpers in qase.pytest.bdd."""

from qase.pytest.bdd import format_data_table, parse_scenario_tags


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
