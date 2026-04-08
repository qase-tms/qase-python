"""Tests for TagParser edge cases, error scenarios, and all tag types."""

from unittest.mock import MagicMock

import pytest

from qase.robotframework.tag_parser import TagParser


class TestParseTagsEmptyAndBasic:
    """Tests for empty input and basic Q-id parsing."""

    def test_empty_tag_list(self):
        metadata = TagParser.parse_tags([])
        assert metadata.qase_ids == []
        assert metadata.ignore is False
        assert metadata.fields == {}
        assert metadata.params == []
        assert metadata.tags == []
        assert metadata.qase_multi_ids == {}

    def test_single_valid_qase_id(self):
        metadata = TagParser.parse_tags(["Q-123"])
        assert metadata.qase_ids == [123]

    def test_multiple_valid_qase_ids(self):
        metadata = TagParser.parse_tags(["Q-1", "Q-2", "Q-99"])
        assert metadata.qase_ids == [1, 2, 99]


class TestParseTagsMalformedIds:
    """Tests for malformed Q-id tags that should be silently ignored."""

    def test_non_numeric_qase_id(self):
        """Q-abc should be silently ignored (regex doesn't match)."""
        metadata = TagParser.parse_tags(["Q-abc"])
        assert metadata.qase_ids == []

    def test_empty_qase_id(self):
        """Q- with no number should be silently ignored."""
        metadata = TagParser.parse_tags(["Q-"])
        assert metadata.qase_ids == []

    def test_decimal_qase_id(self):
        """Q-12.3 should be silently ignored (not a pure integer)."""
        metadata = TagParser.parse_tags(["Q-12.3"])
        assert metadata.qase_ids == []

    def test_qase_id_with_trailing_text(self):
        """Q-123abc should not match (fullmatch required)."""
        metadata = TagParser.parse_tags(["Q-123abc"])
        assert metadata.qase_ids == []


class TestParseTagsIgnore:
    """Tests for qase.ignore tag."""

    def test_ignore_tag(self):
        metadata = TagParser.parse_tags(["qase.ignore"])
        assert metadata.ignore is True

    def test_ignore_tag_case_insensitive(self):
        metadata = TagParser.parse_tags(["QASE.IGNORE"])
        assert metadata.ignore is True

    def test_ignore_tag_mixed_case(self):
        metadata = TagParser.parse_tags(["Qase.Ignore"])
        assert metadata.ignore is True


class TestParseTagsFields:
    """Tests for qase.fields tag with JSON parsing."""

    def test_valid_json_fields(self):
        metadata = TagParser.parse_tags(['qase.fields:{"key":"val"}'])
        assert metadata.fields == {"key": "val"}

    def test_invalid_json_fields_returns_empty_dict(self):
        """Invalid JSON should return empty dict, not crash."""
        metadata = TagParser.parse_tags(["qase.fields:not-json"])
        assert metadata.fields == {}

    def test_invalid_json_fields_with_logger(self):
        """Invalid JSON with logger should call logger.log_error."""
        logger = MagicMock()
        metadata = TagParser.parse_tags(["qase.fields:not-json"], logger=logger)
        assert metadata.fields == {}
        logger.log_error.assert_called_once()

    def test_complex_json_fields(self):
        metadata = TagParser.parse_tags(['qase.fields:{"a":1,"b":"two","c":true}'])
        assert metadata.fields == {"a": 1, "b": "two", "c": True}


class TestParseTagsParams:
    """Tests for qase.params tag."""

    def test_params_with_brackets(self):
        metadata = TagParser.parse_tags(["qase.params:[a,b,c]"])
        assert metadata.params == ["a", "b", "c"]

    def test_params_without_brackets(self):
        metadata = TagParser.parse_tags(["qase.params:x,y"])
        assert metadata.params == ["x", "y"]

    def test_params_single_value(self):
        metadata = TagParser.parse_tags(["qase.params:one"])
        assert metadata.params == ["one"]

    def test_params_empty_value(self):
        """qase.params: with colon but nothing after produces empty from split."""
        metadata = TagParser.parse_tags(["qase.params:"])
        assert metadata.params == []


class TestParseTagsMultiProject:
    """Tests for Q-PROJECT multi-project tags."""

    def test_single_project_single_id(self):
        metadata = TagParser.parse_tags(["Q-PROJECT.PROJ1-123"])
        assert metadata.qase_multi_ids == {"PROJ1": [123]}
        assert metadata.qase_ids == []

    def test_single_project_multiple_ids(self):
        metadata = TagParser.parse_tags(["Q-PROJECT.PROJ1-123,124"])
        assert metadata.qase_multi_ids == {"PROJ1": [123, 124]}

    def test_multiple_projects(self):
        metadata = TagParser.parse_tags([
            "Q-PROJECT.PROJ1-1,2",
            "Q-PROJECT.PROJ2-3",
        ])
        assert metadata.qase_multi_ids == {"PROJ1": [1, 2], "PROJ2": [3]}

    def test_project_non_numeric_ids(self):
        """Q-PROJECT.PROJ1-abc should return empty multi_ids."""
        metadata = TagParser.parse_tags(["Q-PROJECT.PROJ1-abc"])
        assert metadata.qase_multi_ids == {}

    def test_project_missing_ids(self):
        """Q-PROJECT.PROJ1 with no dash-ids should return empty multi_ids."""
        metadata = TagParser.parse_tags(["Q-PROJECT.PROJ1"])
        assert metadata.qase_multi_ids == {}


class TestParseTagsMixed:
    """Tests for multiple mixed tag types in one call."""

    def test_mixed_tags(self):
        metadata = TagParser.parse_tags([
            "Q-42",
            "qase.ignore",
            'qase.fields:{"env":"staging"}',
            "qase.params:[x,y]",
        ])
        assert metadata.qase_ids == [42]
        assert metadata.ignore is True
        assert metadata.fields == {"env": "staging"}
        assert metadata.params == ["x", "y"]

    def test_mixed_project_and_regular_tags(self):
        """Q-PROJECT tags should go to multi_ids, not qase_ids."""
        metadata = TagParser.parse_tags([
            "Q-PROJECT.ABC-10,20",
            "qase.params:[p1]",
        ])
        assert metadata.qase_multi_ids == {"ABC": [10, 20]}
        assert metadata.qase_ids == []
        assert metadata.params == ["p1"]


class TestParseTagsTags:
    """Tests for qase.tags tag."""

    def test_single_tag(self):
        metadata = TagParser.parse_tags(["qase.tags:smoke"])
        assert metadata.tags == ["smoke"]

    def test_multiple_tags(self):
        metadata = TagParser.parse_tags(["qase.tags:smoke,regression,api"])
        assert metadata.tags == ["smoke", "regression", "api"]

    def test_tags_trimmed(self):
        metadata = TagParser.parse_tags(["qase.tags: smoke , regression "])
        assert metadata.tags == ["smoke", "regression"]

    def test_tags_case_insensitive_prefix(self):
        metadata = TagParser.parse_tags(["QASE.TAGS:Smoke"])
        assert metadata.tags == ["Smoke"]

    def test_multiple_tags_entries_accumulated(self):
        metadata = TagParser.parse_tags(["qase.tags:smoke", "qase.tags:regression"])
        assert metadata.tags == ["smoke", "regression"]

    def test_tags_with_other_metadata(self):
        metadata = TagParser.parse_tags([
            "Q-42",
            "qase.tags:smoke,api",
            'qase.fields:{"severity":"blocker"}',
        ])
        assert metadata.qase_ids == [42]
        assert metadata.tags == ["smoke", "api"]
        assert metadata.fields == {"severity": "blocker"}

    def test_empty_tags_value(self):
        metadata = TagParser.parse_tags(["qase.tags:"])
        assert metadata.tags == []
