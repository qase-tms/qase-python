from unittest.mock import MagicMock, patch
from qaseio.commons.report import QaseReport

def test_QaseReport_init():
    report = QaseReport(report_path="custom_path", format="json", environment="env1")
    assert report.report_path == "custom_path"
    assert report.format == "json"
    assert report.environment == "env1"

@patch('os.makedirs')
@patch('shutil.rmtree')
@patch('os.path.exists', return_value=True)
def test_QaseReport_start_run(mock_exists, mock_rmtree, mock_makedirs):
    report = QaseReport()
    report.start_run()
    assert mock_exists.called
    assert mock_rmtree.called
    assert mock_makedirs.called
    assert report.start_time is not None

@patch('os.path.exists', return_value=True)
@patch('shutil.rmtree')
@patch('os.makedirs')
def test_QaseReport_check_report_path(mock_makedirs, mock_rmtree, mock_exists):
    report = QaseReport()
    report._check_report_path()
    assert mock_exists.called
    assert mock_rmtree.called
    assert mock_makedirs.called

@patch('os.path.exists', return_value=True)
@patch('shutil.rmtree')
@patch('os.makedirs')
def test_QaseReport_recreate_dir(mock_makedirs, mock_rmtree, mock_exists):
    report = QaseReport()
    report._recreate_dir("some_path")
    assert mock_exists.called
    assert mock_rmtree.called
    assert mock_makedirs.called

@patch('builtins.open', new_callable=MagicMock)
def test_QaseReport_store_object(mock_open):
    report = QaseReport()
    mock_object = MagicMock()
    mock_object.to_json.return_value = '{"key": "value"}'
    report._store_object(mock_object, "/path", "filename")
    mock_open.assert_called_with("/path/filename.json", "w", encoding="utf-8")