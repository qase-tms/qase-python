import pytest
import tempfile
import os
from qase.behave.qase_global import QaseGlobal, qase
from qase.commons.models import Result
import mimetypes


@pytest.fixture
def qase_global():
    """Fixture for QaseGlobal instance"""
    return QaseGlobal()


@pytest.fixture
def test_scenario():
    """Fixture for test scenario"""
    return Result("Test Scenario", "test_signature")


@pytest.fixture
def qase_with_scenario(qase_global, test_scenario):
    """Fixture for QaseGlobal with active scenario"""
    qase_global._set_current_scenario(test_scenario)
    return qase_global, test_scenario


@pytest.mark.unit
def test_attach_file(qase_with_scenario):
    """Test attaching a file"""
    qase_global, test_scenario = qase_with_scenario
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write("test content")
        temp_path = f.name
    
    try:
        qase_global.attach(file_path=temp_path)
        
        assert len(test_scenario.attachments) == 1
        attachment = test_scenario.attachments[0]
        assert attachment.file_name == os.path.basename(temp_path)
        assert attachment.file_path == temp_path
        assert attachment.content == 'null'
    finally:
        if os.path.exists(temp_path):
            os.unlink(temp_path)


@pytest.mark.unit
def test_attach_content(qase_with_scenario):
    """Test attaching content directly"""
    qase_global, test_scenario = qase_with_scenario
    
    content = "test content"
    qase_global.attach(content=content, file_name="test.txt")
    
    assert len(test_scenario.attachments) == 1
    attachment = test_scenario.attachments[0]
    assert attachment.file_name == "test.txt"
    assert attachment.content == content
    assert attachment.file_path is None


@pytest.mark.unit
def test_attach_binary_content(qase_with_scenario):
    """Test attaching binary content"""
    qase_global, test_scenario = qase_with_scenario
    
    binary_content = b"binary data"
    qase_global.attach(
        content=binary_content,
        file_name="test.bin",
        mime_type="application/octet-stream"
    )
    
    assert len(test_scenario.attachments) == 1
    attachment = test_scenario.attachments[0]
    assert attachment.file_name == "test.bin"
    assert attachment.content == binary_content
    assert attachment.mime_type == "application/octet-stream"


@pytest.mark.unit
def test_auto_detect_mime_type(qase_with_scenario):
    """Test automatic MIME type detection"""
    qase_global, test_scenario = qase_with_scenario
    
    qase_global.attach(content="json data", file_name="data.json")
    
    attachment = test_scenario.attachments[0]
    print(attachment)
    assert attachment.mime_type == "application/json"


@pytest.mark.unit
def test_auto_detect_filename(qase_with_scenario):
    """Test automatic filename detection"""
    qase_global, test_scenario = qase_with_scenario
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write("test content")
        temp_path = f.name
    
    try:
        qase_global.attach(file_path=temp_path)
        
        attachment = test_scenario.attachments[0]
        assert attachment.file_name == os.path.basename(temp_path)
    finally:
        if os.path.exists(temp_path):
            os.unlink(temp_path)


@pytest.mark.unit
def test_no_scenario_error():
    """Test error when no scenario is active"""
    qase_no_scenario = QaseGlobal()
    
    with pytest.raises(RuntimeError, match="No active scenario"):
        qase_no_scenario.attach(content="test")


@pytest.mark.unit
def test_both_file_path_and_content_error(qase_with_scenario):
    """Test error when both file_path and content are provided"""
    qase_global, _ = qase_with_scenario
    
    with pytest.raises(ValueError, match="Either file_path or content must be provided"):
        qase_global.attach(file_path="/path/to/file", content="content")


@pytest.mark.unit
def test_neither_file_path_nor_content_error(qase_with_scenario):
    """Test error when neither file_path nor content is provided"""
    qase_global, _ = qase_with_scenario
    
    with pytest.raises(ValueError, match="Either file_path or content must be provided"):
        qase_global.attach()


@pytest.mark.unit
def test_multiple_attachments(qase_with_scenario):
    """Test adding multiple attachments"""
    qase_global, test_scenario = qase_with_scenario
    
    qase_global.attach(content="first", file_name="first.txt")
    qase_global.attach(content="second", file_name="second.txt")
    
    assert len(test_scenario.attachments) == 2
    assert test_scenario.attachments[0].file_name == "first.txt"
    assert test_scenario.attachments[1].file_name == "second.txt"


@pytest.mark.unit
def test_default_mime_type_for_text(qase_with_scenario):
    """Test default MIME type for text content"""
    qase_global, test_scenario = qase_with_scenario
    
    qase_global.attach(content="plain text")
    
    attachment = test_scenario.attachments[0]
    assert attachment.mime_type == "text/plain"
    assert attachment.file_name == "attachment.txt"


@pytest.mark.unit
def test_default_mime_type_for_binary(qase_with_scenario):
    """Test default MIME type for binary content"""
    qase_global, test_scenario = qase_with_scenario
    
    qase_global.attach(content=b"binary data", file_name="data.bin")
    
    attachment = test_scenario.attachments[0]
    assert attachment.mime_type == "application/octet-stream"


@pytest.mark.unit
def test_attach_with_custom_mime_type(qase_with_scenario):
    """Test attaching with custom MIME type"""
    qase_global, test_scenario = qase_with_scenario
    
    qase_global.attach(
        content="custom content",
        file_name="custom.txt",
        mime_type="application/custom"
    )
    
    attachment = test_scenario.attachments[0]
    assert attachment.mime_type == "application/custom"
    assert attachment.file_name == "custom.txt"


@pytest.mark.unit
def test_attach_file_with_custom_name(qase_with_scenario):
    """Test attaching file with custom name"""
    qase_global, test_scenario = qase_with_scenario
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write("test content")
        temp_path = f.name
    
    try:
        qase_global.attach(file_path=temp_path, file_name="custom_name.txt")
        
        attachment = test_scenario.attachments[0]
        assert attachment.file_name == "custom_name.txt"
        assert attachment.file_path == temp_path
    finally:
        if os.path.exists(temp_path):
            os.unlink(temp_path)


# Comment method tests
@pytest.mark.unit
def test_comment_single_message(qase_with_scenario):
    """Test adding a single comment to scenario"""
    qase_global, test_scenario = qase_with_scenario
    
    qase_global.comment("Test completed successfully")
    
    assert test_scenario.message == "Test completed successfully"


@pytest.mark.unit
def test_comment_multiple_messages(qase_with_scenario):
    """Test adding multiple comments to scenario"""
    qase_global, test_scenario = qase_with_scenario
    
    qase_global.comment("First comment")
    qase_global.comment("Second comment")
    qase_global.comment("Third comment")
    
    expected_message = "First comment\nSecond comment\nThird comment"
    assert test_scenario.message == expected_message


@pytest.mark.unit
def test_comment_empty_message(qase_with_scenario):
    """Test adding empty comment to scenario"""
    qase_global, test_scenario = qase_with_scenario
    
    qase_global.comment("")
    
    assert test_scenario.message == ""


@pytest.mark.unit
def test_comment_with_newlines(qase_with_scenario):
    """Test adding comment with newlines"""
    qase_global, test_scenario = qase_with_scenario
    
    qase_global.comment("Line 1")
    qase_global.comment("Line 2\nWith internal newline")
    qase_global.comment("Line 3")
    
    expected_message = "Line 1\nLine 2\nWith internal newline\nLine 3"
    assert test_scenario.message == expected_message


@pytest.mark.unit
def test_comment_no_scenario_error():
    """Test error when trying to add comment without active scenario"""
    qase_no_scenario = QaseGlobal()
    
    with pytest.raises(RuntimeError, match="No active scenario"):
        qase_no_scenario.comment("test comment")


@pytest.mark.unit
def test_comment_overwrite_existing_message(qase_with_scenario):
    """Test that comment overwrites existing message attribute when message is None"""
    qase_global, test_scenario = qase_with_scenario
    
    # Ensure message is None initially
    test_scenario.message = None
    
    # Add new comment
    qase_global.comment("New comment")
    
    assert test_scenario.message == "New comment"


@pytest.mark.unit
def test_comment_preserves_existing_message(qase_with_scenario):
    """Test that comment preserves existing message when adding multiple"""
    qase_global, test_scenario = qase_with_scenario
    
    # Set existing message
    test_scenario.message = "Existing message"
    
    # Add new comment
    qase_global.comment("Additional comment")
    
    expected_message = "Existing message\nAdditional comment"
    assert test_scenario.message == expected_message 
