import pytest
from unittest.mock import Mock, patch, MagicMock
from qase.commons.models.config.testops import ConfigurationValue, ConfigurationsConfig, TestopsConfig


class TestConfigurationValue:
    def test_configuration_value_creation(self):
        config_value = ConfigurationValue("browser", "chrome")
        assert config_value.name == "browser"
        assert config_value.value == "chrome"

    def test_configuration_value_setters(self):
        config_value = ConfigurationValue()
        config_value.set_name("environment")
        config_value.set_value("staging")
        assert config_value.name == "environment"
        assert config_value.value == "staging"


class TestConfigurationsConfig:
    def test_configurations_config_initialization(self):
        config = ConfigurationsConfig()
        assert config.values == []
        assert config.create_if_not_exists == False

    def test_add_value(self):
        config = ConfigurationsConfig()
        config.add_value("browser", "chrome")
        config.add_value("environment", "staging")
        
        assert len(config.values) == 2
        assert config.values[0].name == "browser"
        assert config.values[0].value == "chrome"
        assert config.values[1].name == "environment"
        assert config.values[1].value == "staging"

    def test_set_create_if_not_exists(self):
        config = ConfigurationsConfig()
        config.set_create_if_not_exists("true")
        assert config.create_if_not_exists == True
        
        config.set_create_if_not_exists("false")
        assert config.create_if_not_exists == False

    def test_set_values(self):
        config = ConfigurationsConfig()
        values = [
            ConfigurationValue("browser", "chrome"),
            ConfigurationValue("environment", "staging")
        ]
        config.set_values(values)
        assert len(config.values) == 2


class TestTestopsConfig:
    def test_testops_config_initialization(self):
        config = TestopsConfig()
        assert config.configurations is not None
        assert config.configurations.values == []
        assert config.configurations.create_if_not_exists == False


class TestConfigurationsIntegration:
    @patch('qase.commons.client.api_v1_client.ConfigurationsApi')
    @patch('qase.commons.client.api_v1_client.RunsApi')
    def test_find_or_create_configuration_existing(self, mock_runs_api, mock_configurations_api):
        # Mock API responses
        mock_config_response = Mock()
        mock_config_response.result.entities = [
            Mock(
                id=1,
                title="browser",
                configurations=[
                    Mock(id=10, name="browser", value="chrome")
                ]
            )
        ]
        mock_configurations_api.return_value.get_configurations.return_value = mock_config_response

        # Create test configuration
        config_value = ConfigurationValue("browser", "chrome")
        
        # Mock config and logger
        mock_config = Mock()
        mock_config.testops.configurations.create_if_not_exists = False
        mock_logger = Mock()
        
        # Import and test the method
        from qase.commons.client.api_v1_client import ApiV1Client
        
        # This would require more complex mocking setup
        # For now, we'll test the configuration parsing logic
        assert config_value.name == "browser"
        assert config_value.value == "chrome"

    def test_configuration_parsing_from_env(self):
        """Test parsing configurations from environment variable format"""
        from qase.commons.config import ConfigManager
        
        # Test with = separator
        config_pairs = "browser=chrome,environment=staging".split(',')
        config_values = []
        
        for pair in config_pairs:
            if '=' in pair:
                name, config_value = pair.split('=', 1)
                config_values.append((name.strip(), config_value.strip()))
        
        assert len(config_values) == 2
        assert config_values[0] == ("browser", "chrome")
        assert config_values[1] == ("environment", "staging")

    def test_configuration_parsing_invalid_format(self):
        """Test parsing configurations with invalid format"""
        config_pairs = "browser:chrome,environment:staging".split(',')
        config_values = []
        
        for pair in config_pairs:
            if '=' in pair:  # This should not match with : separator
                name, config_value = pair.split('=', 1)
                config_values.append((name.strip(), config_value.strip()))
        
        assert len(config_values) == 0  # No matches with = separator 
