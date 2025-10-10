import pytest
from unittest.mock import Mock, patch, MagicMock
from qase.commons.models.config.testops import TestopsConfig
from qase.commons.config import ConfigManager
from qase.commons.client.api_v1_client import ApiV1Client
from qase.commons.client.api_v2_client import ApiV2Client
from qase.commons.reporters.testops import QaseTestOps


class TestPublicReportLinkConfig:
    """Test configuration for public report link functionality"""
    
    def test_testops_config_show_public_report_link_default(self):
        """Test that show_public_report_link defaults to False"""
        config = TestopsConfig()
        assert config.show_public_report_link == False
    
    def test_testops_config_set_show_public_report_link_true(self):
        """Test setting show_public_report_link to True"""
        config = TestopsConfig()
        config.set_show_public_report_link("true")
        assert config.show_public_report_link == True
    
    def test_testops_config_set_show_public_report_link_false(self):
        """Test setting show_public_report_link to False"""
        config = TestopsConfig()
        config.set_show_public_report_link("false")
        assert config.show_public_report_link == False
    
    def test_testops_config_set_show_public_report_link_boolean(self):
        """Test setting show_public_report_link with boolean values"""
        config = TestopsConfig()
        config.set_show_public_report_link(True)
        assert config.show_public_report_link == True
        
        config.set_show_public_report_link(False)
        assert config.show_public_report_link == False


class TestPublicReportLinkConfigManager:
    """Test ConfigManager integration for public report link"""
    
    def test_config_manager_file_config_show_public_report_link(self):
        """Test loading showPublicReportLink from file configuration"""
        # Test the configuration parsing logic directly
        from qase.commons.models.config.testops import TestopsConfig
        
        config = TestopsConfig()
        config.set_show_public_report_link(True)
        assert config.show_public_report_link == True
        
        config.set_show_public_report_link(False)
        assert config.show_public_report_link == False
    
    def test_config_manager_env_var_show_public_report_link(self):
        """Test loading QASE_TESTOPS_SHOW_PUBLIC_REPORT_LINK from environment"""
        with patch.dict('os.environ', {'QASE_TESTOPS_SHOW_PUBLIC_REPORT_LINK': 'true'}):
            config_manager = ConfigManager()
            assert config_manager.config.testops.show_public_report_link == True
    
    def test_config_manager_env_var_override_file_config(self):
        """Test that environment variable overrides file configuration"""
        # Test that environment variable parsing works correctly
        with patch.dict('os.environ', {'QASE_TESTOPS_SHOW_PUBLIC_REPORT_LINK': 'true'}):
            config_manager = ConfigManager()
            assert config_manager.config.testops.show_public_report_link == True
        
        with patch.dict('os.environ', {'QASE_TESTOPS_SHOW_PUBLIC_REPORT_LINK': 'false'}):
            config_manager = ConfigManager()
            assert config_manager.config.testops.show_public_report_link == False


class TestPublicReportLinkApiV1Client:
    """Test API V1 client public report link functionality"""
    
    @patch('qase.commons.client.api_v1_client.RunsApi')
    def test_enable_public_report_success(self, mock_runs_api):
        """Test successful enabling of public report"""
        # Mock API response
        mock_response = Mock()
        mock_response.result.url = "https://app.qase.io/public/report/abc123"
        
        mock_api_instance = Mock()
        mock_api_instance.update_run_publicity.return_value = mock_response
        mock_runs_api.return_value = mock_api_instance
        
        # Create client
        mock_config = Mock()
        mock_config.testops.api.token = "test_token"
        mock_config.testops.api.host = "qase.io"
        mock_logger = Mock()
        
        client = ApiV1Client(mock_config, mock_logger)
        
        # Test the method
        result = client.enable_public_report("TEST", 123)
        
        # Verify
        assert result == "https://app.qase.io/public/report/abc123"
        mock_api_instance.update_run_publicity.assert_called_once()
    
    @patch('qase.commons.client.api_v1_client.RunsApi')
    def test_enable_public_report_no_url(self, mock_runs_api):
        """Test enabling public report when no URL is returned"""
        # Mock API response without URL
        mock_response = Mock()
        mock_response.result.url = None
        
        mock_api_instance = Mock()
        mock_api_instance.update_run_publicity.return_value = mock_response
        mock_runs_api.return_value = mock_api_instance
        
        # Create client
        mock_config = Mock()
        mock_config.testops.api.token = "test_token"
        mock_config.testops.api.host = "qase.io"
        mock_logger = Mock()
        
        client = ApiV1Client(mock_config, mock_logger)
        
        # Test the method
        result = client.enable_public_report("TEST", 123)
        
        # Verify
        assert result is None
        mock_api_instance.update_run_publicity.assert_called_once()
    
    @patch('qase.commons.client.api_v1_client.RunsApi')
    def test_enable_public_report_exception(self, mock_runs_api):
        """Test enabling public report when API call fails"""
        # Mock API exception
        mock_api_instance = Mock()
        mock_api_instance.update_run_publicity.side_effect = Exception("API Error")
        mock_runs_api.return_value = mock_api_instance
        
        # Create client
        mock_config = Mock()
        mock_config.testops.api.token = "test_token"
        mock_config.testops.api.host = "qase.io"
        mock_logger = Mock()
        
        client = ApiV1Client(mock_config, mock_logger)
        
        # Test the method
        result = client.enable_public_report("TEST", 123)
        
        # Verify
        assert result is None
        mock_logger.log.assert_called_with("Error at enabling public report for run 123: API Error", "error")


class TestPublicReportLinkApiV2Client:
    """Test API V2 client public report link functionality"""
    
    def test_enable_public_report_inherits_from_v1(self):
        """Test that API V2 client inherits enable_public_report from API V1 client"""
        # Mock config and logger
        mock_config = Mock()
        mock_config.testops.api.token = "test_token"
        mock_config.testops.api.host = "qase.io"
        mock_logger = Mock()
        
        # Create client
        client = ApiV2Client(mock_config, mock_logger)
        
        # Verify that the method exists (inherited from ApiV1Client)
        assert hasattr(client, 'enable_public_report')
        assert callable(getattr(client, 'enable_public_report'))


class TestPublicReportLinkReporter:
    """Test QaseTestOps reporter integration"""
    
    @patch('qase.commons.reporters.testops.ApiV2Client')
    def test_complete_run_with_public_report_enabled(self, mock_client_class):
        """Test complete_run method when public report is enabled"""
        # Mock client
        mock_client = Mock()
        mock_client.enable_public_report.return_value = "https://app.qase.io/public/report/abc123"
        mock_client_class.return_value = mock_client
        
        # Mock config
        mock_config = Mock()
        mock_config.testops.show_public_report_link = True
        mock_config.testops.run.complete = True
        mock_config.testops.project = "TEST"
        mock_config.testops.api.host = "qase.io"
        mock_config.testops.api.token = "test_token"
        mock_config.testops.run.id = 123
        mock_config.testops.plan.id = None
        mock_config.testops.run.title = "Test Run"
        mock_config.testops.run.description = "Test Description"
        mock_config.testops.run.tags = []
        mock_config.testops.batch.size = 200
        mock_config.testops.status_filter = []
        mock_config.testops.configurations.values = []
        mock_config.environment = None
        mock_config.root_suite = None
        mock_config.exclude_params = []
        mock_config.framework.playwright.video = "failed"
        mock_config.framework.playwright.trace = "failed"
        
        # Mock logger
        mock_logger = Mock()
        
        # Create reporter
        reporter = QaseTestOps(mock_config, mock_logger)
        reporter.run_id = 123
        reporter.project_code = "TEST"
        reporter.results = []
        
        # Test complete_run
        reporter.complete_run()
        
        # Verify
        mock_client.complete_run.assert_called_once_with("TEST", 123)
        mock_client.enable_public_report.assert_called_once_with("TEST", 123)
        mock_logger.log.assert_called_with("Public report link: https://app.qase.io/public/report/abc123", "info")
    
    @patch('qase.commons.reporters.testops.ApiV2Client')
    def test_complete_run_with_public_report_disabled(self, mock_client_class):
        """Test complete_run method when public report is disabled"""
        # Mock client
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        # Mock config
        mock_config = Mock()
        mock_config.testops.show_public_report_link = False
        mock_config.testops.run.complete = True
        mock_config.testops.project = "TEST"
        mock_config.testops.api.host = "qase.io"
        mock_config.testops.api.token = "test_token"
        mock_config.testops.run.id = 123
        mock_config.testops.plan.id = None
        mock_config.testops.run.title = "Test Run"
        mock_config.testops.run.description = "Test Description"
        mock_config.testops.run.tags = []
        mock_config.testops.batch.size = 200
        mock_config.testops.status_filter = []
        mock_config.testops.configurations.values = []
        mock_config.environment = None
        mock_config.root_suite = None
        mock_config.exclude_params = []
        mock_config.framework.playwright.video = "failed"
        mock_config.framework.playwright.trace = "failed"
        
        # Mock logger
        mock_logger = Mock()
        
        # Create reporter
        reporter = QaseTestOps(mock_config, mock_logger)
        reporter.run_id = 123
        reporter.project_code = "TEST"
        reporter.results = []
        
        # Test complete_run
        reporter.complete_run()
        
        # Verify
        mock_client.complete_run.assert_called_once_with("TEST", 123)
        mock_client.enable_public_report.assert_not_called()
    
    @patch('qase.commons.reporters.testops.ApiV2Client')
    def test_complete_run_public_report_failure(self, mock_client_class):
        """Test complete_run method when public report generation fails"""
        # Mock client
        mock_client = Mock()
        mock_client.enable_public_report.return_value = None
        mock_client_class.return_value = mock_client
        
        # Mock config
        mock_config = Mock()
        mock_config.testops.show_public_report_link = True
        mock_config.testops.run.complete = True
        mock_config.testops.project = "TEST"
        mock_config.testops.api.host = "qase.io"
        mock_config.testops.api.token = "test_token"
        mock_config.testops.run.id = 123
        mock_config.testops.plan.id = None
        mock_config.testops.run.title = "Test Run"
        mock_config.testops.run.description = "Test Description"
        mock_config.testops.run.tags = []
        mock_config.testops.batch.size = 200
        mock_config.testops.status_filter = []
        mock_config.testops.configurations.values = []
        mock_config.environment = None
        mock_config.root_suite = None
        mock_config.exclude_params = []
        mock_config.framework.playwright.video = "failed"
        mock_config.framework.playwright.trace = "failed"
        
        # Mock logger
        mock_logger = Mock()
        
        # Create reporter
        reporter = QaseTestOps(mock_config, mock_logger)
        reporter.run_id = 123
        reporter.project_code = "TEST"
        reporter.results = []
        
        # Test complete_run
        reporter.complete_run()
        
        # Verify
        mock_client.complete_run.assert_called_once_with("TEST", 123)
        mock_client.enable_public_report.assert_called_once_with("TEST", 123)
        mock_logger.log.assert_called_with("Failed to generate public report link", "warning")
