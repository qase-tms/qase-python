import pytest
from pathlib import Path
from qaseio.commons import QaseReport

def test_init_default_values():
    report = QaseReport()
    assert report.report_path == "build/qase-report"
    assert report.format == "json"
    assert report.results == []
    assert report.attachments == {}

def test_init_custom_values():
    report = QaseReport(report_path="custom/report-path", format="xml")
    assert report.report_path == "custom/report-path"
    assert report.format == "xml"

def test_check_report_path(tmpdir):
    report_path = str(tmpdir.join("qase-report"))
    report = QaseReport(report_path=report_path)
    assert Path(report_path).is_dir()

def test_add_result():
    report = QaseReport()
    result = "PASSED"
    steps = [{"action": "Open app", "expected": "App is opened"}]
    report.add_result(result, steps)
    # Add assertions once the 'add_result' method is implemented
    # assert report.results == [...]

def test_start_run():
    report = QaseReport()
    report.start_run()
    # Add assertions once the 'start_run' method is implemented
    # assert ...

def test_complete_run():
    report = QaseReport()
    report.complete_run()
    # Add assertions once the 'complete_run' method is implemented
    # assert ...