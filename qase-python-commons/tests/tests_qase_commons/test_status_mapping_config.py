"""
Tests for status mapping configuration integration.
"""

import pytest
import json
import tempfile
import os
from unittest.mock import Mock, patch
from qase.commons.config import ConfigManager
from qase.commons.models.config.qaseconfig import QaseConfig
from qase.commons.reporters.core import QaseCoreReporter
from qase.commons.models.result import Result, Execution


class TestStatusMappingConfig:
    """Test cases for status mapping configuration."""

    def test_qase_config_status_mapping_initialization(self):
        """Test QaseConfig initialization with status mapping."""
        config = QaseConfig()
        assert config.status_mapping == {}
        assert isinstance(config.status_mapping, dict)

    def test_qase_config_set_status_mapping(self):
        """Test setting status mapping in QaseConfig."""
        config = QaseConfig()
        mapping = {"invalid": "failed", "skipped": "passed"}
        config.set_status_mapping(mapping)
        assert config.status_mapping == mapping

    def test_config_manager_load_status_mapping_from_file(self):
        """Test loading status mapping from config file."""
        config_data = {
            "statusMapping": {
                "invalid": "failed",
                "skipped": "passed"
            }
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config_data, f)
            config_file = f.name
        
        try:
            config_manager = ConfigManager(config_file)
            assert config_manager.config.status_mapping == config_data["statusMapping"]
        finally:
            os.unlink(config_file)

    def test_config_manager_load_status_mapping_from_env(self):
        """Test loading status mapping from environment variable."""
        env_value = "invalid=failed,skipped=passed"
        
        with patch.dict(os.environ, {'QASE_STATUS_MAPPING': env_value}):
            config_manager = ConfigManager()
            expected = {"invalid": "failed", "skipped": "passed"}
            assert config_manager.config.status_mapping == expected

    def test_config_manager_env_overrides_file(self):
        """Test that environment variable overrides file configuration."""
        config_data = {
            "statusMapping": {
                "invalid": "blocked"
            }
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config_data, f)
            config_file = f.name
        
        try:
            env_value = "invalid=failed"
            with patch.dict(os.environ, {'QASE_STATUS_MAPPING': env_value}):
                config_manager = ConfigManager(config_file)
                expected = {"invalid": "failed"}
                assert config_manager.config.status_mapping == expected
        finally:
            os.unlink(config_file)

    def test_config_manager_empty_status_mapping(self):
        """Test handling of empty status mapping."""
        config_data = {}
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config_data, f)
            config_file = f.name
        
        try:
            config_manager = ConfigManager(config_file)
            assert config_manager.config.status_mapping == {}
        finally:
            os.unlink(config_file)

    def test_config_manager_invalid_status_mapping_format(self):
        """Test handling of invalid status mapping format in file."""
        config_data = {
            "statusMapping": "invalid=failed"  # Should be dict, not string
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config_data, f)
            config_file = f.name
        
        try:
            config_manager = ConfigManager(config_file)
            # Should still work, just set the string as mapping
            assert config_manager.config.status_mapping == "invalid=failed"
        finally:
            os.unlink(config_file)


class TestStatusMappingReporterIntegration:
    """Test cases for status mapping integration with reporters."""

    def test_qase_core_reporter_status_mapping_initialization(self):
        """Test QaseCoreReporter initialization with status mapping."""
        config_data = {
            "statusMapping": {
                "invalid": "failed",
                "skipped": "passed"
            },
            "mode": "off"
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config_data, f)
            config_file = f.name
        
        try:
            config_manager = ConfigManager(config_file)
            reporter = QaseCoreReporter(config_manager)
            
            # Check that status mapping was initialized
            assert not reporter.status_mapping.is_empty()
            assert reporter.status_mapping.mapping == config_data["statusMapping"]
        finally:
            os.unlink(config_file)

    def test_qase_core_reporter_status_mapping_empty(self):
        """Test QaseCoreReporter initialization with empty status mapping."""
        config_data = {"mode": "off"}
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config_data, f)
            config_file = f.name
        
        try:
            config_manager = ConfigManager(config_file)
            reporter = QaseCoreReporter(config_manager)
            
            # Check that status mapping is empty
            assert reporter.status_mapping.is_empty()
        finally:
            os.unlink(config_file)

    def test_apply_status_mapping_to_result(self):
        """Test applying status mapping to test result."""
        config_data = {
            "statusMapping": {
                "invalid": "failed",
                "skipped": "passed"
            },
            "mode": "off"
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config_data, f)
            config_file = f.name
        
        try:
            config_manager = ConfigManager(config_file)
            reporter = QaseCoreReporter(config_manager)
            
            # Create test result with invalid status
            result = Result("Test Title", "test_signature")
            result.execution.set_status("invalid")
            
            # Apply status mapping
            reporter._apply_status_mapping(result)
            
            # Check that status was mapped
            assert result.get_status() == "failed"
        finally:
            os.unlink(config_file)

    def test_apply_status_mapping_no_change(self):
        """Test applying status mapping when no mapping exists."""
        config_data = {
            "statusMapping": {
                "invalid": "failed"
            },
            "mode": "off"
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config_data, f)
            config_file = f.name
        
        try:
            config_manager = ConfigManager(config_file)
            reporter = QaseCoreReporter(config_manager)
            
            # Create test result with status that has no mapping
            result = Result("Test Title", "test_signature")
            result.execution.set_status("passed")
            
            # Apply status mapping
            reporter._apply_status_mapping(result)
            
            # Check that status was not changed
            assert result.get_status() == "passed"
        finally:
            os.unlink(config_file)

    def test_apply_status_mapping_empty_status(self):
        """Test applying status mapping to result with empty status."""
        config_data = {
            "statusMapping": {
                "invalid": "failed"
            },
            "mode": "off"
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config_data, f)
            config_file = f.name
        
        try:
            config_manager = ConfigManager(config_file)
            reporter = QaseCoreReporter(config_manager)
            
            # Create test result with no status
            result = Result("Test Title", "test_signature")
            
            # Apply status mapping
            reporter._apply_status_mapping(result)
            
            # Check that status remains None
            assert result.get_status() is None
        finally:
            os.unlink(config_file)

    def test_apply_status_mapping_logging(self):
        """Test that status mapping changes are logged."""
        config_data = {
            "statusMapping": {
                "invalid": "failed"
            },
            "mode": "off",
            "debug": True
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config_data, f)
            config_file = f.name
        
        try:
            config_manager = ConfigManager(config_file)
            reporter = QaseCoreReporter(config_manager)
            
            # Create test result
            result = Result("Test Title", "test_signature")
            result.execution.set_status("invalid")
            
            # Mock logger to verify debug message
            with patch.object(reporter.logger, 'log_debug') as mock_log_debug:
                reporter._apply_status_mapping(result)
                mock_log_debug.assert_called_with("Status mapped for 'Test Title': invalid -> failed")
        finally:
            os.unlink(config_file)


class TestStatusMappingEdgeCases:
    """Test edge cases for status mapping configuration."""

    def test_status_mapping_with_all_valid_statuses(self):
        """Test status mapping with all valid statuses."""
        mapping = {
            "passed": "passed",
            "failed": "failed", 
            "skipped": "skipped",
            "disabled": "disabled",
            "blocked": "blocked",
            "invalid": "invalid"
        }
        
        config_data = {
            "statusMapping": mapping,
            "mode": "off"
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config_data, f)
            config_file = f.name
        
        try:
            config_manager = ConfigManager(config_file)
            reporter = QaseCoreReporter(config_manager)
            
            # Test each status
            for original_status in mapping.keys():
                result = Result(f"Test {original_status}", "test_signature")
                result.execution.set_status(original_status)
                reporter._apply_status_mapping(result)
                assert result.get_status() == mapping[original_status]
        finally:
            os.unlink(config_file)

    def test_status_mapping_chain(self):
        """Test chained status mappings."""
        config_data = {
            "statusMapping": {
                "invalid": "skipped",
                "skipped": "passed"
            },
            "mode": "off"
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config_data, f)
            config_file = f.name
        
        try:
            config_manager = ConfigManager(config_file)
            reporter = QaseCoreReporter(config_manager)
            
            # Test that only first mapping is applied (no chaining)
            result = Result("Test Title", "test_signature")
            result.execution.set_status("invalid")
            reporter._apply_status_mapping(result)
            
            # Should map to "skipped", not "passed"
            assert result.get_status() == "skipped"
        finally:
            os.unlink(config_file)

    def test_status_mapping_case_sensitivity(self):
        """Test that status mapping configuration is case sensitive."""
        # Test that configuration with uppercase status names fails validation
        config_data = {
            "statusMapping": {
                "INVALID": "failed"  # Uppercase - should cause validation error
            },
            "mode": "off"
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config_data, f)
            config_file = f.name
        
        try:
            # This should raise an exception because "INVALID" is not a valid status
            with pytest.raises(Exception):  # StatusMappingError will be raised
                config_manager = ConfigManager(config_file)
                reporter = QaseCoreReporter(config_manager)
        finally:
            os.unlink(config_file)
        
        # Test that lowercase configuration works
        config_data_lower = {
            "statusMapping": {
                "invalid": "failed"  # Lowercase - valid status
            },
            "mode": "off"
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config_data_lower, f)
            config_file = f.name
        
        try:
            config_manager = ConfigManager(config_file)
            reporter = QaseCoreReporter(config_manager)
            
            # Test with lowercase status - should map
            result = Result("Test Title", "test_signature")
            result.execution.set_status("invalid")  # Lowercase
            reporter._apply_status_mapping(result)
            
            # Should map because case matches
            assert result.get_status() == "failed"
        finally:
            os.unlink(config_file)
