from qase.tavern.plugin import QasePytestPlugin


def test_extract_qase_id_with_valid_id():
    text = "QaseID=123 Some text"
    qase_ids, project_ids, remaining_text = QasePytestPlugin.extract_qase_ids(text)
    assert qase_ids == [123]
    assert project_ids == {}
    assert remaining_text == "Some text"

def test_extract_multiple_qase_id_with_valid_id():
    text = "QaseID=123,321 Some text"
    qase_ids, project_ids, remaining_text = QasePytestPlugin.extract_qase_ids(text)
    assert qase_ids == [123,321]
    assert project_ids == {}
    assert remaining_text == "Some text"

def test_extract_qase_id_with_valid_id_lowercase():
    text = "qaseid=456 More text"
    qase_ids, project_ids, remaining_text = QasePytestPlugin.extract_qase_ids(text)
    assert qase_ids == [456]
    assert project_ids == {}
    assert remaining_text == "More text"


def test_extract_qase_id_with_no_qaseid():
    text = "No QaseID here"
    qase_ids, project_ids, remaining_text = QasePytestPlugin.extract_qase_ids(text)
    assert qase_ids == []
    assert project_ids == {}
    assert remaining_text == text


def test_extract_qase_id_with_spaces():
    text = "   QaseID= 321   Text with spaces   "
    qase_ids, project_ids, remaining_text = QasePytestPlugin.extract_qase_ids(text)
    assert qase_ids == [321]
    assert project_ids == {}
    assert remaining_text == "Text with spaces"


def test_extract_qase_id_with_only_qaseid():
    text = "QaseID=999"
    qase_ids, project_ids, remaining_text = QasePytestPlugin.extract_qase_ids(text)
    assert qase_ids == [999]
    assert project_ids == {}
    assert remaining_text == ""


def test_extract_qase_id_with_special_characters():
    text = "Some text QaseID=123!@#$"
    qase_ids, project_ids, remaining_text = QasePytestPlugin.extract_qase_ids(text)
    assert qase_ids == [123]
    assert project_ids == {}
    assert remaining_text == "Some text !@#$"


def test_extract_qase_id_with_empty_string():
    text = ""
    qase_ids, project_ids, remaining_text = QasePytestPlugin.extract_qase_ids(text)
    assert qase_ids == []
    assert project_ids == {}
    assert remaining_text == ""


def test_extract_project_ids():
    text = "QaseProjectID.PROJ1=123,124 Some text"
    qase_ids, project_ids, remaining_text = QasePytestPlugin.extract_qase_ids(text)
    assert qase_ids == []
    assert project_ids == {"PROJ1": [123, 124]}
    assert remaining_text == "Some text"


def test_extract_multiple_project_ids():
    text = "QaseProjectID.PROJ1=123 QaseProjectID.PROJ2=456 Some text"
    qase_ids, project_ids, remaining_text = QasePytestPlugin.extract_qase_ids(text)
    assert qase_ids == []
    assert project_ids == {"PROJ1": [123], "PROJ2": [456]}
    assert remaining_text == "Some text"
