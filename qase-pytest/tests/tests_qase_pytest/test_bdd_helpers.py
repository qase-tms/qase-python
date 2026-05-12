"""Unit tests for pure helpers in qase.pytest.bdd."""

from qase.pytest.bdd import parse_scenario_tags


class TestParseScenarioTags:
    def test_empty_returns_empty_dict(self):
        result = parse_scenario_tags([])
        assert result == {
            "testops_ids": None,
            "testops_project_mapping": None,
            "ignore": False,
            "muted": False,
            "suite": None,
            "fields": {},
            "tags": [],
        }

    def test_qase_id_single(self):
        result = parse_scenario_tags(["qase.id=42"])
        assert result["testops_ids"] == [42]

    def test_qase_id_multiple(self):
        result = parse_scenario_tags(["qase.id=42,43,44"])
        assert result["testops_ids"] == [42, 43, 44]

    def test_qase_id_multiple_with_spaces(self):
        result = parse_scenario_tags(["qase.id=42, 43 ,44"])
        assert result["testops_ids"] == [42, 43, 44]

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
