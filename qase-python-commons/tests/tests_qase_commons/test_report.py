from unittest.mock import MagicMock, patch
from qase.commons.reporters import QaseReport
from qase.commons.config import ConfigManager
from qase.commons.logger import Logger
from qase.commons.models.config.connection import Format


def test_QaseReport_init():
    logger = Logger()
    config = ConfigManager()
    config.config.report.connection.path = "custom_path"
    config.config.report.connection.format = Format.json
    config.config.environment = "env1"

    report = QaseReport(config, logger)
    assert report.report_path == "custom_path"
    assert report.format == Format.json
    assert report.environment == "env1"


@patch('os.makedirs')
@patch('shutil.rmtree')
@patch('os.path.exists', return_value=True)
def test_QaseReport_start_run(mock_exists, mock_rmtree, mock_makedirs):
    logger = Logger()
    config = ConfigManager()
    report = QaseReport(config, logger)
    report.start_run()
    assert mock_exists.called
    assert mock_rmtree.called
    assert mock_makedirs.called
    assert report.start_time is not None


@patch('os.path.exists', return_value=True)
@patch('shutil.rmtree')
@patch('os.makedirs')
def test_QaseReport_check_report_path(mock_makedirs, mock_rmtree, mock_exists):
    logger = Logger()
    config = ConfigManager()
    report = QaseReport(config, logger)
    report._check_report_path()
    assert mock_exists.called
    assert mock_rmtree.called
    assert mock_makedirs.called


@patch('os.path.exists', return_value=True)
@patch('shutil.rmtree')
@patch('os.makedirs')
def test_QaseReport_recreate_dir(mock_makedirs, mock_rmtree, mock_exists):
    logger = Logger()
    config = ConfigManager()
    report = QaseReport(config, logger)
    report._recreate_dir("some_path")
    assert mock_exists.called
    assert mock_rmtree.called
    assert mock_makedirs.called


@patch('builtins.open', new_callable=MagicMock)
def test_QaseReport_store_object(mock_open):
    logger = Logger()
    config = ConfigManager()
    report = QaseReport(config, logger)
    mock_object = MagicMock()
    mock_object.to_json.return_value = '{"key": "value"}'
    report._store_object(mock_object, "/path", "filename")
    mock_open.assert_called_with("/path/filename.json", "w", encoding="utf-8")
