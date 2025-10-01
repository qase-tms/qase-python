import pytest
import os
import json
import tempfile
from unittest.mock import patch, mock_open
from qase.commons.models.config.qaseconfig import LoggingConfig, QaseConfig


class TestLoggingConfig:
    def test_logging_config_initialization(self):
        config = LoggingConfig()
        assert config.console is None
        assert config.file is None

    def test_set_console(self):
        config = LoggingConfig()
        config.set_console(True)
        assert config.console == True
        
        config.set_console(False)
        assert config.console == False

    def test_set_file(self):
        config = LoggingConfig()
        config.set_file(True)
        assert config.file == True
        
        config.set_file(False)
        assert config.file == False


class TestQaseConfigLogging:
    def test_qase_config_logging_initialization(self):
        config = QaseConfig()
        assert config.logging is not None
        assert isinstance(config.logging, LoggingConfig)

    def test_set_logging(self):
        config = QaseConfig()
        logging_config = {
            "console": True,
            "file": False
        }
        config.set_logging(logging_config)
        
        assert config.logging.console == True
        assert config.logging.file == False

    def test_set_logging_partial(self):
        config = QaseConfig()
        logging_config = {
            "console": True
        }
        config.set_logging(logging_config)
        
        assert config.logging.console == True
        assert config.logging.file is None  # Should remain unchanged

    def test_set_logging_none_values(self):
        config = QaseConfig()
        logging_config = {
            "console": None,
            "file": None
        }
        config.set_logging(logging_config)
        
        assert config.logging.console is None
        assert config.logging.file is None


class TestConfigManagerLogging:
    def test_config_manager_logging_from_file(self):
        from qase.commons.config import ConfigManager
        
        config_data = {
            "debug": True,
            "logging": {
                "console": False,
                "file": True
            }
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config_data, f)
            config_file = f.name
        
        try:
            config_manager = ConfigManager(config_file)
            
            assert config_manager.config.debug == True
            assert config_manager.config.logging.console == False
            assert config_manager.config.logging.file == True
            
            # Check that logger is initialized with correct options
            assert config_manager.logger.logging_options.console == False
            assert config_manager.logger.logging_options.file == True
            
        finally:
            os.unlink(config_file)

    def test_config_manager_logging_from_env(self):
        from qase.commons.config import ConfigManager
        
        with patch.dict(os.environ, {
            'QASE_LOGGING_CONSOLE': 'false',
            'QASE_LOGGING_FILE': 'true'
        }):
            config_manager = ConfigManager()
            
            # Environment variables are now parsed as boolean by QaseUtils.parse_bool()
            assert config_manager.config.logging.console == False
            assert config_manager.config.logging.file == True
            
            # Check that logger is initialized with correct options (parsed as boolean)
            assert config_manager.logger.logging_options.console == False
            assert config_manager.logger.logging_options.file == True

    def test_config_manager_logging_env_override_file(self):
        from qase.commons.config import ConfigManager
        
        config_data = {
            "logging": {
                "console": True,
                "file": False
            }
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config_data, f)
            config_file = f.name
        
        try:
            with patch.dict(os.environ, {
                'QASE_LOGGING_CONSOLE': 'false',
                'QASE_LOGGING_FILE': 'true'
            }):
                config_manager = ConfigManager(config_file)
                
                # Environment variables are now parsed as boolean by QaseUtils.parse_bool()
                assert config_manager.config.logging.console == False
                assert config_manager.config.logging.file == True
                
        finally:
            os.unlink(config_file)

    def test_config_manager_logging_default_behavior(self):
        from qase.commons.config import ConfigManager
        
        config_manager = ConfigManager()
        
        # Default behavior: console enabled, file disabled (unless debug)
        assert config_manager.config.logging.console is None
        assert config_manager.config.logging.file is None
        
        # Logger should use defaults
        assert config_manager.logger.logging_options.console == True
        assert config_manager.logger.logging_options.file == False

    def test_config_manager_logging_debug_mode(self):
        from qase.commons.config import ConfigManager
        
        config_data = {
            "debug": True
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config_data, f)
            config_file = f.name
        
        try:
            config_manager = ConfigManager(config_file)
            
            assert config_manager.config.debug == True
            
            # Logger should enable file logging in debug mode
            assert config_manager.logger.logging_options.console == True
            assert config_manager.logger.logging_options.file == True
            
        finally:
            os.unlink(config_file)

    def test_config_manager_logging_debug_env_var(self):
        from qase.commons.config import ConfigManager
        
        with patch.dict(os.environ, {'QASE_DEBUG': 'true'}):
            config_manager = ConfigManager()
            
            assert config_manager.config.debug == True
            
            # Logger should enable file logging when debug is enabled via env
            assert config_manager.logger.logging_options.console == True
            assert config_manager.logger.logging_options.file == True

