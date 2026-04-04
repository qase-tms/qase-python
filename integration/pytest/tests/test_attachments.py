"""Tests demonstrating attachment functionality."""
import json
import os

from qase.pytest import qase


@qase.id(601)
@qase.title("Test with file attachment")
def test_file_attachment():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    attachments_dir = os.path.join(current_dir, "..", "attachments")
    qase.attach(os.path.join(attachments_dir, "sample.txt"))
    assert True


@qase.id(602)
@qase.title("Test with bytes attachment")
def test_bytes_attachment():
    content = json.dumps({"key": "value"}, indent=2).encode("utf-8")
    qase.attach((content, "application/json", "data.json"))
    assert True


@qase.id(603)
@qase.title("Test with attachment in step")
def test_attachment_in_step():
    with qase.step("Step with attachment"):
        qase.attach((b"step log content", "text/plain", "step.log"))
    assert True
