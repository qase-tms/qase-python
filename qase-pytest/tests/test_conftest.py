import re

TEST_FILE = """
from qaseio.pytest import qase
@qase.id(1)
def test_example():
    pass
"""


def test_run_all_parameters_cli(mock, default_mocks, testdir):
    default_mocks()
    testdir.makepyfile(
        """
    def test_example():
        pass
    """
    )
    result = testdir.runpytest(
        "--qase",
        "--qase-project=PRJ",
        "--qase-testrun=3",
        "--qase-api-token=12345",
        "--qase-debug",
    )
    assert result.ret == 0
    assert len(mock.request_history) == 2
    assert re.findall(r".*/project/PRJ", mock.request_history[0].url)
    assert re.findall(r".*/run/PRJ/3", mock.request_history[1].url)
    assert mock.request_history[0].headers.get("Token") == "12345"


def test_run_create_testrun_no_ids(mock, default_mocks, testdir):
    default_mocks()
    testdir.makepyfile(
        """
    from qaseio.pytest import qase
    def test_example():
        qase.attach((b'', "text/plain", "example.txt"))
    """
    )
    result = testdir.runpytest(
        "--qase",
        "--qase-project=PRJ",
        "--qase-new-run",
        "--qase-api-token=12345",
        "--qase-debug",
    )
    assert result.ret == 0
    assert len(mock.request_history) == 1
    assert re.findall(r".*/project/PRJ", mock.request_history[0].url)
    assert mock.request_history[0].headers.get("Token") == "12345"


def test_run_create_testrun(
    mock, default_mocks, cases_mocks, results_mocks, attachment_mocks, testdir
):
    default_mocks()
    cases_mocks()
    results_mocks()
    attachment_mocks()
    testdir.makepyfile(
        """
    from qaseio.pytest import qase
    @qase.id(1)
    def test_example():
        qase.attach((b'{}', "text/plain", "example.txt"))
    """
    )
    result = testdir.runpytest(
        "--qase",
        "--qase-project=PRJ",
        "--qase-new-run",
        "--qase-api-token=12345",
        "--qase-debug",
    )
    assert result.ret == 0
    assert len(mock.request_history) == 7
    assert re.findall(r".*/project/PRJ", mock.request_history[0].url)
    assert mock.request_history[0].headers.get("Token") == "12345"


def test_run_create_testrun_and_id(mock, default_mocks, testdir):
    default_mocks()
    testdir.makepyfile(TEST_FILE)
    result = testdir.runpytest(
        "--qase",
        "--qase-project=PRJ",
        "--qase-testrun=3",
        "--qase-new-run",
        "--qase-api-token=12345",
        "--qase-debug",
    )
    assert result.ret != 0
    assert len(mock.request_history) == 2


def test_run_create_testrun_and_testplan(mock, default_mocks, testdir):
    default_mocks()
    testdir.makepyfile(TEST_FILE)
    result = testdir.runpytest(
        "--qase",
        "--qase-project=PRJ",
        "--qase-testplan=3",
        "--qase-new-run",
        "--qase-api-token=12345",
        "--qase-debug",
    )
    assert result.ret != 0
    assert len(mock.request_history) == 1


def test_run_testrun_and_testplan(mock, default_mocks, testdir):
    default_mocks()
    testdir.makepyfile(TEST_FILE)
    result = testdir.runpytest(
        "--qase",
        "--qase-project=PRJ",
        "--qase-testplan=3",
        "--qase-testrun=4",
        "--qase-api-token=12345",
        "--qase-debug",
    )
    assert result.ret != 0
    assert len(mock.request_history) == 1


def test_run_testrun_and_create_testrun_and_testplan(
    mock, default_mocks, testdir
):
    default_mocks()
    testdir.makepyfile(TEST_FILE)
    result = testdir.runpytest(
        "--qase",
        "--qase-project=PRJ",
        "--qase-testplan=3",
        "--qase-testrun=4",
        "--qase-new-run",
        "--qase-api-token=12345",
        "--qase-debug",
    )
    assert result.ret != 0
    assert len(mock.request_history) == 1


def test_run_not_enabled(mock, default_mocks, testdir):
    default_mocks()
    testdir.makepyfile(
        """
    from qaseio.pytest import qase
    def test_example():
        qase.attach((b'', "text/plain", "example.txt"))
    """
    )
    result = testdir.runpytest()
    assert result.ret == 0
    assert not mock.called
    assert len(mock.request_history) == 0


def test_run_all_parameters_config(mock, default_mocks, testdir):
    default_mocks()
    testdir.makepyfile(
        """
    def test_example():
        pass
    """
    )
    testdir.makefile(
        ".ini",
        pytest=(
            "[pytest]\nqs_enabled=True\nqs_project_code=PRJ\n"
            "qs_testrun_id=3\nqs_api_token=12345\nqs_debug=True"
        ),
    )
    result = testdir.runpytest()
    assert result.ret == 0
    assert len(mock.request_history) == 2
    assert re.findall(r".*/project/PRJ", mock.request_history[0].url)
    assert re.findall(r".*/run/PRJ/3", mock.request_history[1].url)
    assert mock.request_history[0].headers.get("Token") == "12345"


def test_run_override_using_cli(mock, default_mocks, testdir):
    default_mocks()
    testdir.makepyfile(
        """
    def test_example():
        pass
    """
    )
    testdir.makefile(
        ".ini",
        pytest=(
            "[pytest]\nqs_enabled=True\nqs_project_code=PRJCODE\n"
            "qs_testrun_id=1\nqs_api_token=12345\nqs_debug=True"
        ),
    )
    result = testdir.runpytest(
        "--qase-project=PRJ",
        "--qase-testrun=3",
        "--qase-api-token=45678",
    )
    assert result.ret == 0
    assert len(mock.request_history) == 2
    assert re.findall(r".*/project/PRJ", mock.request_history[0].url)
    assert re.findall(r".*/run/PRJ/3", mock.request_history[1].url)
    assert mock.request_history[0].headers.get("Token") == "45678"
