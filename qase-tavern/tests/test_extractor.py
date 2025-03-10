from qase.tavern.plugin import QasePytestPlugin


def test_extract_qase_id_with_valid_id():
    text = "QaseID=123 Some text"
    qase_id, remaining_text = QasePytestPlugin.extract_qase_id(text)
    assert qase_id == [123]
    assert remaining_text == "Some text"

def test_extract_multiple_qase_id_with_valid_id():
    text = "QaseID=123,321 Some text"
    qase_id, remaining_text = QasePytestPlugin.extract_qase_id(text)
    assert qase_id == [123,321]
    assert remaining_text == "Some text"

def test_extract_qase_id_with_valid_id_lowercase():
    text = "qaseid=456 More text"
    qase_id, remaining_text = QasePytestPlugin.extract_qase_id(text)
    assert qase_id == [456]
    assert remaining_text == "More text"


def test_extract_qase_id_with_no_qaseid():
    text = "No QaseID here"
    qase_id, remaining_text = QasePytestPlugin.extract_qase_id(text)
    assert qase_id == []
    assert remaining_text == text


def test_extract_qase_id_with_spaces():
    text = "   QaseID= 321   Text with spaces   "
    qase_id, remaining_text = QasePytestPlugin.extract_qase_id(text)
    assert qase_id == [321]
    assert remaining_text == "Text with spaces"


def test_extract_qase_id_with_only_qaseid():
    text = "QaseID=999"
    qase_id, remaining_text = QasePytestPlugin.extract_qase_id(text)
    assert qase_id == [999]
    assert remaining_text == ""


def test_extract_qase_id_with_special_characters():
    text = "Some text QaseID=123!@#$"
    qase_id, remaining_text = QasePytestPlugin.extract_qase_id(text)
    assert qase_id == [123]
    assert remaining_text == "Some text !@#$"


def test_extract_qase_id_with_empty_string():
    text = ""
    qase_id, remaining_text = QasePytestPlugin.extract_qase_id(text)
    assert qase_id == []
    assert remaining_text == ""
