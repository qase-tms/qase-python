"""
Tests for TestopsMultiConfig and ProjectConfig models.
"""
import pytest
from qase.commons.models.config.testops import ProjectConfig, TestopsMultiConfig, RunConfig, PlanConfig


class TestProjectConfig:
    """Test cases for ProjectConfig model."""

    def test_project_config_initialization(self):
        """Test ProjectConfig initialization with default values."""
        config = ProjectConfig()
        
        assert config.code is None
        assert config.run is not None
        assert isinstance(config.run, RunConfig)
        assert config.plan is not None
        assert isinstance(config.plan, PlanConfig)
        assert config.environment is None

    def test_project_config_set_code(self):
        """Test setting project code."""
        config = ProjectConfig()
        config.set_code("PROJ1")
        
        assert config.code == "PROJ1"

    def test_project_config_set_environment(self):
        """Test setting environment."""
        config = ProjectConfig()
        config.set_environment("staging")
        
        assert config.environment == "staging"

    def test_project_config_set_run_from_dict(self):
        """Test setting run configuration from dictionary."""
        config = ProjectConfig()
        run_dict = {
            "title": "Test Run",
            "description": "Description",
            "complete": True,
            "id": 123,
            "tags": ["tag1", "tag2"]
        }
        config.set_run(run_dict)
        
        assert config.run.title == "Test Run"
        assert config.run.description == "Description"
        assert config.run.complete is True
        assert config.run.id == 123
        assert config.run.tags == ["tag1", "tag2"]

    def test_project_config_set_run_partial(self):
        """Test setting run configuration with partial dictionary."""
        config = ProjectConfig()
        run_dict = {
            "title": "Test Run",
            "complete": False
        }
        config.set_run(run_dict)
        
        assert config.run.title == "Test Run"
        assert config.run.complete is False
        assert config.run.description is None

    def test_project_config_set_plan_from_dict(self):
        """Test setting plan configuration from dictionary."""
        config = ProjectConfig()
        plan_dict = {"id": 456}
        config.set_plan(plan_dict)
        
        assert config.plan.id == 456

    def test_project_config_set_plan_empty(self):
        """Test setting plan configuration with empty dictionary."""
        config = ProjectConfig()
        config.set_plan({})
        
        assert config.plan.id is None


class TestTestopsMultiConfig:
    """Test cases for TestopsMultiConfig model."""

    def test_testops_multi_config_initialization(self):
        """Test TestopsMultiConfig initialization with default values."""
        config = TestopsMultiConfig()
        
        assert config.default_project is None
        assert config.projects is not None
        assert isinstance(config.projects, list)
        assert len(config.projects) == 0

    def test_testops_multi_config_set_default_project(self):
        """Test setting default project."""
        config = TestopsMultiConfig()
        config.set_default_project("PROJ1")
        
        assert config.default_project == "PROJ1"

    def test_testops_multi_config_set_projects(self):
        """Test setting projects list."""
        config = TestopsMultiConfig()
        
        project1 = ProjectConfig()
        project1.set_code("PROJ1")
        
        project2 = ProjectConfig()
        project2.set_code("PROJ2")
        
        config.set_projects([project1, project2])
        
        assert len(config.projects) == 2
        assert config.projects[0].code == "PROJ1"
        assert config.projects[1].code == "PROJ2"

    def test_testops_multi_config_add_project(self):
        """Test adding project to the list."""
        config = TestopsMultiConfig()
        
        project1 = ProjectConfig()
        project1.set_code("PROJ1")
        config.add_project(project1)
        
        project2 = ProjectConfig()
        project2.set_code("PROJ2")
        config.add_project(project2)
        
        assert len(config.projects) == 2
        assert config.projects[0].code == "PROJ1"
        assert config.projects[1].code == "PROJ2"

    def test_testops_multi_config_empty_projects(self):
        """Test that projects list can be empty."""
        config = TestopsMultiConfig()
        config.set_projects([])
        
        assert len(config.projects) == 0
