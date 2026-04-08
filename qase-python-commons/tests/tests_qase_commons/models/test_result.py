"""
Tests for Result model, including multi-project support.
"""
import pytest
from qase.commons.models.result import Result


class TestResultProjectMapping:
    """Test cases for Result model project mapping functionality."""

    def test_result_initialization_without_mapping(self):
        """Test that Result initializes without project mapping."""
        result = Result("Test Title", "test_signature")
        assert result.testops_project_mapping is None
        assert result.testops_ids is None

    def test_set_testops_project_mapping_single_project(self):
        """Test setting project mapping for a single project."""
        result = Result("Test Title", "test_signature")
        result.set_testops_project_mapping("PROJ1", [123, 124])
        
        assert result.testops_project_mapping is not None
        assert result.testops_project_mapping["PROJ1"] == [123, 124]

    def test_set_testops_project_mapping_multiple_projects(self):
        """Test setting project mapping for multiple projects."""
        result = Result("Test Title", "test_signature")
        result.set_testops_project_mapping("PROJ1", [123, 124])
        result.set_testops_project_mapping("PROJ2", [456, 457])
        
        assert result.testops_project_mapping is not None
        assert result.testops_project_mapping["PROJ1"] == [123, 124]
        assert result.testops_project_mapping["PROJ2"] == [456, 457]

    def test_set_testops_project_mapping_overwrite(self):
        """Test that setting mapping for same project overwrites previous values."""
        result = Result("Test Title", "test_signature")
        result.set_testops_project_mapping("PROJ1", [123, 124])
        result.set_testops_project_mapping("PROJ1", [999])
        
        assert result.testops_project_mapping["PROJ1"] == [999]

    def test_get_testops_project_mapping_empty(self):
        """Test getting project mapping when it's empty."""
        result = Result("Test Title", "test_signature")
        assert result.get_testops_project_mapping() is None

    def test_get_testops_project_mapping_with_data(self):
        """Test getting project mapping with data."""
        result = Result("Test Title", "test_signature")
        result.set_testops_project_mapping("PROJ1", [123, 124])
        result.set_testops_project_mapping("PROJ2", [456])
        
        mapping = result.get_testops_project_mapping()
        assert mapping is not None
        assert mapping == {"PROJ1": [123, 124], "PROJ2": [456]}

    def test_get_testops_ids_for_project_existing(self):
        """Test getting IDs for an existing project."""
        result = Result("Test Title", "test_signature")
        result.set_testops_project_mapping("PROJ1", [123, 124])
        
        ids = result.get_testops_ids_for_project("PROJ1")
        assert ids == [123, 124]

    def test_get_testops_ids_for_project_nonexistent(self):
        """Test getting IDs for a non-existent project."""
        result = Result("Test Title", "test_signature")
        result.set_testops_project_mapping("PROJ1", [123, 124])
        
        ids = result.get_testops_ids_for_project("PROJ2")
        assert ids is None

    def test_get_testops_ids_for_project_no_mapping(self):
        """Test getting IDs when mapping is None."""
        result = Result("Test Title", "test_signature")
        
        ids = result.get_testops_ids_for_project("PROJ1")
        assert ids is None

    def test_get_projects_empty(self):
        """Test getting projects list when mapping is empty."""
        result = Result("Test Title", "test_signature")
        
        projects = result.get_projects()
        assert projects == []

    def test_get_projects_single(self):
        """Test getting projects list with single project."""
        result = Result("Test Title", "test_signature")
        result.set_testops_project_mapping("PROJ1", [123, 124])
        
        projects = result.get_projects()
        assert projects == ["PROJ1"]

    def test_get_projects_multiple(self):
        """Test getting projects list with multiple projects."""
        result = Result("Test Title", "test_signature")
        result.set_testops_project_mapping("PROJ1", [123, 124])
        result.set_testops_project_mapping("PROJ2", [456])
        result.set_testops_project_mapping("PROJ3", [789, 790])
        
        projects = result.get_projects()
        assert len(projects) == 3
        assert "PROJ1" in projects
        assert "PROJ2" in projects
        assert "PROJ3" in projects

    def test_backward_compatibility_testops_ids(self):
        """Test that backward compatibility with testops_ids is maintained."""
        result = Result("Test Title", "test_signature")
        result.testops_ids = [123, 124]
        
        assert result.get_testops_ids() == [123, 124]
        assert result.testops_project_mapping is None

    def test_project_mapping_and_testops_ids_coexist(self):
        """Test that project mapping and testops_ids can coexist."""
        result = Result("Test Title", "test_signature")
        result.testops_ids = [999]  # Old single-project IDs
        result.set_testops_project_mapping("PROJ1", [123, 124])  # New multi-project

        assert result.get_testops_ids() == [999]
        assert result.get_testops_project_mapping() == {"PROJ1": [123, 124]}


class TestResultTags:
    """Test cases for Result model tags functionality."""

    def test_result_initializes_with_empty_tags(self):
        result = Result("Test Title", "test_signature")
        assert result.tags == []

    def test_add_single_tag(self):
        result = Result("Test Title", "test_signature")
        result.add_tag("smoke")
        assert result.tags == ["smoke"]

    def test_add_multiple_tags(self):
        result = Result("Test Title", "test_signature")
        result.add_tag("smoke")
        result.add_tag("regression")
        assert "smoke" in result.tags
        assert "regression" in result.tags

    def test_add_tag_deduplication(self):
        result = Result("Test Title", "test_signature")
        result.add_tag("smoke")
        result.add_tag("smoke")
        assert result.tags == ["smoke"]

    def test_add_tag_empty_string_ignored(self):
        result = Result("Test Title", "test_signature")
        result.add_tag("")
        assert result.tags == []

    def test_add_tags_list(self):
        result = Result("Test Title", "test_signature")
        result.add_tags(["smoke", "regression", "api"])
        assert "smoke" in result.tags
        assert "regression" in result.tags
        assert "api" in result.tags

    def test_add_tags_list_deduplication(self):
        result = Result("Test Title", "test_signature")
        result.add_tags(["smoke", "smoke", "regression"])
        assert result.tags == ["smoke", "regression"]

    def test_get_tags(self):
        result = Result("Test Title", "test_signature")
        result.add_tag("smoke")
        result.add_tag("regression")
        assert result.get_tags() == ["smoke", "regression"]

    def test_add_tags_accumulates(self):
        result = Result("Test Title", "test_signature")
        result.add_tags(["smoke"])
        result.add_tags(["regression"])
        assert "smoke" in result.tags
        assert "regression" in result.tags


class TestResultTagsFieldsMerge:
    """Test tags merge into fields for API mapping."""

    def test_tags_written_to_fields(self):
        result = Result("Test", "sig")
        result.add_tags(["smoke", "regression"])
        # Simulate merge logic
        existing_str = result.fields.get("tags", "")
        existing = [t.strip() for t in existing_str.split(",") if t.strip()] if existing_str else []
        all_tags = list(dict.fromkeys(existing + result.tags))
        result.fields["tags"] = ",".join(all_tags)
        assert result.fields["tags"] == "smoke,regression"

    def test_tags_merge_with_existing_fields_tags(self):
        result = Result("Test", "sig")
        result.fields["tags"] = "fromfield"
        result.add_tags(["smoke", "api"])
        existing_str = result.fields.get("tags", "")
        existing = [t.strip() for t in existing_str.split(",") if t.strip()] if existing_str else []
        all_tags = list(dict.fromkeys(existing + result.tags))
        result.fields["tags"] = ",".join(all_tags)
        assert result.fields["tags"] == "fromfield,smoke,api"

    def test_tags_merge_deduplication(self):
        result = Result("Test", "sig")
        result.fields["tags"] = "smoke,regression"
        result.add_tags(["smoke", "api"])
        existing_str = result.fields.get("tags", "")
        existing = [t.strip() for t in existing_str.split(",") if t.strip()] if existing_str else []
        all_tags = list(dict.fromkeys(existing + result.tags))
        result.fields["tags"] = ",".join(all_tags)
        assert result.fields["tags"] == "smoke,regression,api"

    def test_empty_tags_no_field_written(self):
        result = Result("Test", "sig")
        assert "tags" not in result.fields
