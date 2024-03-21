import os

from qaseio.pytest import qase


def test_with_bytes_attachment_success():
    qase.attach((str.encode("This is a simple string attachment"), "text/plain", "simple.txt"))
    assert 1 == 1


def test_with_bytes_attachment_failed():
    qase.attach((str.encode("This is a simple string attachment"), "text/plain", "simple.txt"))
    assert 1 == 2


def test_with_file_attachment_success():
    current_directory = os.getcwd()
    qase.attach(f"{current_directory}/attachments/file.txt",
                f"{current_directory}/attachments/image.png")
    assert 1 == 1


def test_with_file_attachment_failed():
    current_directory = os.getcwd()
    qase.attach(f"{current_directory}/attachments/file.txt",
                f"{current_directory}/attachments/image.png")
    assert 1 == 2


def test_with_file_attachment_and_mime_tipe_success():
    current_directory = os.getcwd()
    qase.attach(
        (f"{current_directory}/attachments/file.txt", "text/plain"))
    assert 1 == 1


def test_with_file_attachment_and_mime_tipe_failed():
    current_directory = os.getcwd()
    qase.attach(
        (f"{current_directory}/attachments/file.txt", "text/plain"))
    assert 1 == 2


@qase.step("Step with bytes attachment")
def step_with_bytes_attachment():
    qase.attach((str.encode("This is a simple string attachment"), "text/plain", "simple.txt"))
    pass


def test_with_step_attachment_success():
    step_with_bytes_attachment()
    assert 1 == 1


def test_with_step_attachment_failed():
    step_with_bytes_attachment()
    assert 1 == 2
