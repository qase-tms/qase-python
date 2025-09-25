"""
Tests for status mapping functionality.
"""

import pytest
import os
from unittest.mock import Mock, patch
from qase.commons.status_mapping.status_mapping import StatusMapping, StatusMappingError, create_status_mapping_from_config, create_status_mapping_from_env


class TestStatusMapping:
    """Test cases for StatusMapping class."""

    def test_status_mapping_initialization_empty(self):
        """Test initialization with empty mapping."""
        mapping = StatusMapping()
        assert mapping.mapping == {}
        assert mapping.is_empty()

    def test_status_mapping_initialization_with_dict(self):
        """Test initialization with mapping dictionary."""
        mapping_dict = {"invalid": "failed", "skipped": "passed"}
        mapping = StatusMapping(mapping_dict)
        assert mapping.mapping == mapping_dict
        assert not mapping.is_empty()

    def test_from_dict_valid_mapping(self):
        """Test creating StatusMapping from valid dictionary."""
        mapping_dict = {"invalid": "failed", "skipped": "passed"}
        mapping = StatusMapping.from_dict(mapping_dict)
        assert mapping.mapping == mapping_dict

    def test_from_dict_invalid_source_status(self):
        """Test creating StatusMapping with invalid source status."""
        mapping_dict = {"invalid_status": "failed"}
        with pytest.raises(StatusMappingError, match="Invalid source status"):
            StatusMapping.from_dict(mapping_dict)

    def test_from_dict_invalid_target_status(self):
        """Test creating StatusMapping with invalid target status."""
        mapping_dict = {"invalid": "invalid_status"}
        with pytest.raises(StatusMappingError, match="Invalid target status"):
            StatusMapping.from_dict(mapping_dict)

    def test_from_env_string_valid(self):
        """Test creating StatusMapping from valid environment string."""
        env_string = "invalid=failed,skipped=passed"
        mapping = StatusMapping.from_env_string(env_string)
        expected = {"invalid": "failed", "skipped": "passed"}
        assert mapping.mapping == expected

    def test_from_env_string_empty(self):
        """Test creating StatusMapping from empty environment string."""
        mapping = StatusMapping.from_env_string("")
        assert mapping.mapping == {}
        assert mapping.is_empty()

    def test_from_env_string_none(self):
        """Test creating StatusMapping from None environment string."""
        mapping = StatusMapping.from_env_string(None)
        assert mapping.mapping == {}
        assert mapping.is_empty()

    def test_from_env_string_invalid_format(self):
        """Test creating StatusMapping from invalid environment string format."""
        env_string = "invalid:failed"
        with pytest.raises(StatusMappingError, match="Invalid mapping format"):
            StatusMapping.from_env_string(env_string)

    def test_from_env_string_empty_status(self):
        """Test creating StatusMapping with empty status values."""
        env_string = "=failed"
        with pytest.raises(StatusMappingError, match="Empty status in mapping"):
            StatusMapping.from_env_string(env_string)

    def test_set_mapping_valid(self):
        """Test setting valid mapping."""
        mapping = StatusMapping()
        mapping_dict = {"invalid": "failed", "skipped": "passed"}
        mapping.set_mapping(mapping_dict)
        assert mapping.mapping == mapping_dict

    def test_set_mapping_invalid_type(self):
        """Test setting mapping with invalid type."""
        mapping = StatusMapping()
        with pytest.raises(StatusMappingError, match="Mapping must be a dictionary"):
            mapping.set_mapping("invalid")

    def test_parse_env_string_with_spaces(self):
        """Test parsing environment string with spaces."""
        env_string = " invalid = failed , skipped = passed "
        mapping = StatusMapping()
        mapping.parse_env_string(env_string)
        expected = {"invalid": "failed", "skipped": "passed"}
        assert mapping.mapping == expected

    def test_parse_env_string_with_empty_pairs(self):
        """Test parsing environment string with empty pairs."""
        env_string = "invalid=failed,,skipped=passed"
        mapping = StatusMapping()
        mapping.parse_env_string(env_string)
        expected = {"invalid": "failed", "skipped": "passed"}
        assert mapping.mapping == expected

    def test_apply_mapping_existing(self):
        """Test applying mapping for existing status."""
        mapping = StatusMapping({"invalid": "failed"})
        result = mapping.apply_mapping("invalid")
        assert result == "failed"

    def test_apply_mapping_non_existing(self):
        """Test applying mapping for non-existing status."""
        mapping = StatusMapping({"invalid": "failed"})
        result = mapping.apply_mapping("passed")
        assert result == "passed"

    def test_apply_mapping_empty_status(self):
        """Test applying mapping for empty status."""
        mapping = StatusMapping({"invalid": "failed"})
        result = mapping.apply_mapping("")
        assert result == ""

    def test_apply_mapping_none_status(self):
        """Test applying mapping for None status."""
        mapping = StatusMapping({"invalid": "failed"})
        result = mapping.apply_mapping(None)
        assert result is None

    def test_get_mapping(self):
        """Test getting mapping copy."""
        mapping_dict = {"invalid": "failed", "skipped": "passed"}
        mapping = StatusMapping(mapping_dict)
        result = mapping.get_mapping()
        assert result == mapping_dict
        # Ensure it's a copy, not the same object
        assert result is not mapping.mapping

    def test_validate_valid_mapping(self):
        """Test validation of valid mapping."""
        mapping = StatusMapping({"invalid": "failed", "skipped": "passed"})
        errors = mapping.validate()
        assert len(errors) == 0

    def test_validate_invalid_mapping(self):
        """Test validation of invalid mapping."""
        mapping = StatusMapping({"invalid_status": "failed", "skipped": "invalid_target"})
        errors = mapping.validate()
        assert len(errors) == 2
        assert "Invalid source status: invalid_status" in errors
        assert "Invalid target status: invalid_target" in errors

    def test_str_representation(self):
        """Test string representation."""
        mapping_dict = {"invalid": "failed"}
        mapping = StatusMapping(mapping_dict)
        assert str(mapping) == str(mapping_dict)

    def test_repr_representation(self):
        """Test detailed string representation."""
        mapping_dict = {"invalid": "failed"}
        mapping = StatusMapping(mapping_dict)
        assert "StatusMapping" in repr(mapping)
        assert str(mapping_dict) in repr(mapping)


class TestStatusMappingHelpers:
    """Test cases for helper functions."""

    def test_create_status_mapping_from_config_valid(self):
        """Test creating StatusMapping from valid config."""
        config_value = {"invalid": "failed", "skipped": "passed"}
        mapping = create_status_mapping_from_config(config_value)
        assert mapping.mapping == config_value

    def test_create_status_mapping_from_config_none(self):
        """Test creating StatusMapping from None config."""
        mapping = create_status_mapping_from_config(None)
        assert mapping.mapping == {}
        assert mapping.is_empty()

    def test_create_status_mapping_from_config_empty(self):
        """Test creating StatusMapping from empty config."""
        mapping = create_status_mapping_from_config({})
        assert mapping.mapping == {}
        assert mapping.is_empty()

    @patch.dict(os.environ, {'STATUS_MAPPING': 'invalid=failed,skipped=passed'})
    def test_create_status_mapping_from_env_with_value(self):
        """Test creating StatusMapping from environment variable with value."""
        mapping = create_status_mapping_from_env()
        expected = {"invalid": "failed", "skipped": "passed"}
        assert mapping.mapping == expected

    @patch.dict(os.environ, {}, clear=True)
    def test_create_status_mapping_from_env_without_value(self):
        """Test creating StatusMapping from environment variable without value."""
        mapping = create_status_mapping_from_env()
        assert mapping.mapping == {}
        assert mapping.is_empty()

    @patch.dict(os.environ, {'CUSTOM_STATUS_MAPPING': 'invalid=failed'})
    def test_create_status_mapping_from_env_custom_var(self):
        """Test creating StatusMapping from custom environment variable."""
        mapping = create_status_mapping_from_env('CUSTOM_STATUS_MAPPING')
        expected = {"invalid": "failed"}
        assert mapping.mapping == expected


class TestStatusMappingIntegration:
    """Integration tests for status mapping functionality."""

    def test_valid_statuses(self):
        """Test that all valid statuses are recognized."""
        valid_statuses = StatusMapping.VALID_STATUSES
        expected_statuses = {'passed', 'failed', 'skipped', 'disabled', 'blocked', 'invalid'}
        assert valid_statuses == expected_statuses

    def test_mapping_all_valid_statuses(self):
        """Test mapping with all valid statuses."""
        mapping_dict = {
            'passed': 'passed',
            'failed': 'failed',
            'skipped': 'skipped',
            'disabled': 'disabled',
            'blocked': 'blocked',
            'invalid': 'invalid'
        }
        mapping = StatusMapping.from_dict(mapping_dict)
        assert mapping.validate() == []

    def test_complex_mapping_scenario(self):
        """Test complex mapping scenario."""
        env_string = "invalid=failed,skipped=passed,disabled=skipped"
        mapping = StatusMapping.from_env_string(env_string)
        
        # Test multiple mappings
        assert mapping.apply_mapping("invalid") == "failed"
        assert mapping.apply_mapping("skipped") == "passed"
        assert mapping.apply_mapping("disabled") == "skipped"
        assert mapping.apply_mapping("passed") == "passed"  # No mapping
        assert mapping.apply_mapping("failed") == "failed"  # No mapping

    def test_logging_integration(self):
        """Test that logging works correctly."""
        mapping = StatusMapping({"invalid": "failed"})
        
        # Mock logger to verify debug messages
        with patch.object(mapping.logger, 'debug') as mock_debug:
            mapping.apply_mapping("invalid")
            mock_debug.assert_called_once_with("Status mapped: invalid -> failed")

    def test_error_handling_edge_cases(self):
        """Test error handling for edge cases."""
        # Test with non-string values
        with pytest.raises(StatusMappingError):
            StatusMapping.from_dict({123: "failed"})
        
        # Test with non-string target
        with pytest.raises(StatusMappingError):
            StatusMapping.from_dict({"invalid": 123})
