"""
Tests for QaseTestOpsMulti reporter.
"""
import pytest
from unittest.mock import Mock, MagicMock, patch
from qase.commons.reporters.testops_multi import QaseTestOpsMulti
from qase.commons.models.result import Result
from qase.commons.models.config.testops import ProjectConfig, TestopsMultiConfig
from qase.commons.models.config.qaseconfig import QaseConfig, Mode


class TestQaseTestOpsMulti:
    """Test cases for QaseTestOpsMulti reporter."""

    def _create_mock_config(self):
        """Helper to create mock configuration."""
        mock_config = Mock(spec=QaseConfig)
        mock_config.mode = Mode.testops_multi
        mock_config.testops = Mock()
        mock_config.testops.api = Mock()
        mock_config.testops.api.host = "qase.io"
        mock_config.testops.api.token = "test_token"
        mock_config.testops.batch = Mock()
        mock_config.testops.batch.size = 200
        mock_config.testops.status_filter = []
        mock_config.testops.show_public_report_link = False
        mock_config.environment = None
        
        # Create multi-config
        mock_config.testops_multi = TestopsMultiConfig()
        mock_config.testops_multi.set_default_project("PROJ1")
        
        # Add projects
        project1 = ProjectConfig()
        project1.set_code("PROJ1")
        project1.run.set_title("Project 1 Run")
        project1.run.set_description("Description 1")
        
        project2 = ProjectConfig()
        project2.set_code("PROJ2")
        project2.run.set_title("Project 2 Run")
        project2.run.set_description("Description 2")
        
        mock_config.testops_multi.set_projects([project1, project2])
        
        return mock_config

    def _create_mock_client(self):
        """Helper to create mock API client."""
        mock_client = Mock()
        mock_client.get_project.return_value = None
        mock_client.get_environment.return_value = None
        mock_client.check_test_run.return_value = True
        mock_client.create_test_run.return_value = 123
        mock_client.send_results = Mock()
        mock_client.complete_run = Mock()
        return mock_client

    def test_init_with_multiple_projects(self):
        """Test initialization with multiple projects."""
        mock_config = self._create_mock_config()
        mock_logger = Mock()
        mock_client = self._create_mock_client()
        
        reporter = QaseTestOpsMulti(mock_config, mock_logger, mock_client)
        
        assert len(reporter.project_configs) == 2
        assert "PROJ1" in reporter.project_configs
        assert "PROJ2" in reporter.project_configs
        assert len(reporter.project_results) == 2
        assert "PROJ1" in reporter.project_results
        assert "PROJ2" in reporter.project_results

    def test_start_run_creates_runs_for_all_projects(self):
        """Test that start_run creates runs for all projects."""
        mock_config = self._create_mock_config()
        mock_logger = Mock()
        mock_client = self._create_mock_client()
        mock_client.create_test_run.side_effect = [123, 456]
        
        reporter = QaseTestOpsMulti(mock_config, mock_logger, mock_client)
        run_ids = reporter.start_run()
        
        assert len(run_ids) == 2
        assert run_ids["PROJ1"] == 123
        assert run_ids["PROJ2"] == 456
        assert mock_client.create_test_run.call_count == 2

    def test_start_run_with_existing_run_id(self):
        """Test start_run with existing run IDs in config."""
        mock_config = self._create_mock_config()
        mock_config.testops_multi.projects[0].run.set_id(999)
        mock_logger = Mock()
        mock_client = self._create_mock_client()
        
        reporter = QaseTestOpsMulti(mock_config, mock_logger, mock_client)
        run_ids = reporter.start_run()
        
        assert run_ids["PROJ1"] == 999
        mock_client.check_test_run.assert_called_with("PROJ1", 999)
        mock_client.create_test_run.assert_called_once()  # Only for PROJ2

    def test_start_run_with_plan_id(self):
        """Test start_run with test plan ID."""
        mock_config = self._create_mock_config()
        mock_config.testops_multi.projects[0].plan.set_id(789)
        mock_logger = Mock()
        mock_client = self._create_mock_client()
        mock_client.create_test_run.return_value = 123
        
        reporter = QaseTestOpsMulti(mock_config, mock_logger, mock_client)
        run_ids = reporter.start_run()
        
        # Verify create_test_run was called with plan_id for PROJ1
        calls = mock_client.create_test_run.call_args_list
        assert any("plan_id" in str(call) or call[1].get("plan_id") == 789 for call in calls)

    def test_set_run_id(self):
        """Test setting run ID for a project."""
        mock_config = self._create_mock_config()
        mock_logger = Mock()
        mock_client = self._create_mock_client()
        
        reporter = QaseTestOpsMulti(mock_config, mock_logger, mock_client)
        # Initialize project_runs with project codes (normally done in start_run)
        # But set_run_id can be called before start_run, so we need to handle it
        reporter.project_runs["PROJ1"] = None
        reporter.set_run_id("PROJ1", "123")
        
        assert reporter.project_runs["PROJ1"] == 123
        # Verify logger was not called (no warning)
        mock_logger.log.assert_not_called()

    def test_set_run_id_string_conversion(self):
        """Test that set_run_id converts string to int."""
        mock_config = self._create_mock_config()
        mock_logger = Mock()
        mock_client = self._create_mock_client()
        
        reporter = QaseTestOpsMulti(mock_config, mock_logger, mock_client)
        # Initialize project_runs with project codes (normally done in start_run)
        reporter.project_runs["PROJ1"] = None
        reporter.set_run_id("PROJ1", "456")
        
        assert isinstance(reporter.project_runs["PROJ1"], int)
        assert reporter.project_runs["PROJ1"] == 456
        # Verify logger was not called (no warning)
        mock_logger.log.assert_not_called()

    def test_set_run_id_unknown_project(self):
        """Test that set_run_id logs warning for unknown project."""
        mock_config = self._create_mock_config()
        mock_logger = Mock()
        mock_client = self._create_mock_client()
        
        reporter = QaseTestOpsMulti(mock_config, mock_logger, mock_client)
        reporter.set_run_id("UNKNOWN_PROJ", "123")
        
        # Verify warning was logged
        mock_logger.log.assert_called_once()
        call_args = mock_logger.log.call_args
        assert "Unknown project code" in call_args[0][0]
        assert "warning" in call_args[0] or call_args[1].get("level") == "warning"

    def test_add_result_with_project_mapping(self):
        """Test adding result with project mapping."""
        mock_config = self._create_mock_config()
        mock_logger = Mock()
        mock_client = self._create_mock_client()
        
        reporter = QaseTestOpsMulti(mock_config, mock_logger, mock_client)
        reporter.start_run()
        
        result = Result("Test Title", "test_signature")
        result.set_testops_project_mapping("PROJ1", [123, 124])
        result.set_testops_project_mapping("PROJ2", [456])
        
        reporter.add_result(result)
        
        # Results should be added to both projects
        assert len(reporter.project_results["PROJ1"]) == 1
        assert len(reporter.project_results["PROJ2"]) == 1

    def test_add_result_without_mapping_uses_default(self):
        """Test adding result without mapping uses default project."""
        mock_config = self._create_mock_config()
        mock_logger = Mock()
        mock_client = self._create_mock_client()
        
        reporter = QaseTestOpsMulti(mock_config, mock_logger, mock_client)
        reporter.start_run()
        
        result = Result("Test Title", "test_signature")
        result.testops_ids = [999]  # Old single-project IDs
        
        reporter.add_result(result)
        
        # Should go to default project (PROJ1)
        assert len(reporter.project_results["PROJ1"]) == 1
        assert len(reporter.project_results["PROJ2"]) == 0

    def test_add_result_without_mapping_no_default_uses_first(self):
        """Test adding result without mapping and no default uses first project."""
        mock_config = self._create_mock_config()
        mock_config.testops_multi.default_project = None
        mock_logger = Mock()
        mock_client = self._create_mock_client()
        
        reporter = QaseTestOpsMulti(mock_config, mock_logger, mock_client)
        reporter.start_run()
        
        result = Result("Test Title", "test_signature")
        
        reporter.add_result(result)
        
        # Should go to first project (PROJ1)
        assert len(reporter.project_results["PROJ1"]) == 1

    def test_add_result_creates_project_specific_copies(self):
        """Test that add_result creates separate copies for each project."""
        mock_config = self._create_mock_config()
        mock_logger = Mock()
        mock_client = self._create_mock_client()
        
        reporter = QaseTestOpsMulti(mock_config, mock_logger, mock_client)
        reporter.start_run()
        
        result = Result("Test Title", "test_signature")
        result.set_testops_project_mapping("PROJ1", [123])
        result.set_testops_project_mapping("PROJ2", [456])
        
        reporter.add_result(result)
        
        # Verify copies have correct testops_ids
        proj1_result = reporter.project_results["PROJ1"][0]
        proj2_result = reporter.project_results["PROJ2"][0]
        
        assert proj1_result.testops_ids == [123]
        assert proj2_result.testops_ids == [456]
        assert proj1_result.testops_project_mapping is None
        assert proj2_result.testops_project_mapping is None

    def test_create_project_result(self):
        """Test _create_project_result method."""
        mock_config = self._create_mock_config()
        mock_logger = Mock()
        mock_client = self._create_mock_client()
        
        reporter = QaseTestOpsMulti(mock_config, mock_logger, mock_client)
        
        original_result = Result("Test Title", "test_signature")
        original_result.set_testops_project_mapping("PROJ1", [123])
        original_result.set_testops_project_mapping("PROJ2", [456])
        
        project_result = reporter._create_project_result(original_result, "PROJ1", [123])
        
        assert project_result.testops_ids == [123]
        assert project_result.testops_project_mapping is None
        assert project_result.title == "Test Title"
        # Verify they are different objects (deepcopy creates new object)
        assert id(project_result) != id(original_result)
        # Verify modifying one doesn't affect the other
        project_result.title = "Modified Title"
        assert original_result.title == "Test Title"

    def test_create_project_result_with_none_ids(self):
        """Test _create_project_result with None IDs."""
        mock_config = self._create_mock_config()
        mock_logger = Mock()
        mock_client = self._create_mock_client()
        
        reporter = QaseTestOpsMulti(mock_config, mock_logger, mock_client)
        
        original_result = Result("Test Title", "test_signature")
        project_result = reporter._create_project_result(original_result, "PROJ1", None)
        
        assert project_result.testops_ids is None

    def test_send_results_for_project(self):
        """Test sending results for a specific project."""
        mock_config = self._create_mock_config()
        mock_logger = Mock()
        mock_client = self._create_mock_client()
        
        reporter = QaseTestOpsMulti(mock_config, mock_logger, mock_client)
        reporter.start_run()
        
        result = Result("Test Title", "test_signature")
        result.set_testops_project_mapping("PROJ1", [123])
        reporter.add_result(result)
        
        # Manually trigger send (normally done by batch size or complete_run)
        reporter._send_results_for_project("PROJ1")
        
        # Wait a bit for thread to complete
        import time
        time.sleep(0.1)
        
        # Verify results were sent
        assert len(reporter.project_results["PROJ1"]) == 0  # Queue cleared
        mock_client.send_results.assert_called()

    def test_complete_run_sends_remaining_results(self):
        """Test that complete_run sends remaining results."""
        mock_config = self._create_mock_config()
        mock_logger = Mock()
        mock_client = self._create_mock_client()
        
        reporter = QaseTestOpsMulti(mock_config, mock_logger, mock_client)
        reporter.start_run()
        
        result = Result("Test Title", "test_signature")
        result.set_testops_project_mapping("PROJ1", [123])
        reporter.add_result(result)
        
        reporter.complete_run()
        
        # Wait for threads
        import time
        time.sleep(0.2)
        
        # Verify complete_run was called
        mock_client.complete_run.assert_called()

    def test_complete_run_with_public_report(self):
        """Test complete_run with public report enabled."""
        mock_config = self._create_mock_config()
        mock_config.testops.show_public_report_link = True
        mock_logger = Mock()
        mock_client = self._create_mock_client()
        mock_client.enable_public_report.return_value = "https://app.qase.io/public/report/abc123"
        
        reporter = QaseTestOpsMulti(mock_config, mock_logger, mock_client)
        reporter.start_run()
        
        reporter.complete_run()
        
        # Wait for threads
        import time
        time.sleep(0.2)
        
        # Verify public report was enabled
        mock_client.enable_public_report.assert_called()
