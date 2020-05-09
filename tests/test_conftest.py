import re


def test_run_all_parameters_cli(mock, default_mocks, testdir):
    default_mocks()
    testdir.makepyfile(
        """
    def test_example():
        pass
    """
    )
    testdir.runpytest(
        "--qase",
        "--qase-project=PRJ",
        "--qase-testrun=3",
        "--qase-api-token=12345",
        "--qase-debug",
    )
    assert len(mock.request_history) == 2
    assert re.findall(r".*/project/PRJ", mock.request_history[0].url)
    assert re.findall(r".*/run/PRJ/3", mock.request_history[1].url)
    assert mock.request_history[0].headers.get("Token") == "12345"


def test_run_not_enabled(mock, default_mocks, testdir):
    default_mocks()
    testdir.makepyfile(
        """
    def test_example():
        pass
    """
    )
    testdir.runpytest()
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
    testdir.runpytest()
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
    testdir.runpytest(
        "--qase-project=PRJ", "--qase-testrun=3", "--qase-api-token=45678",
    )
    assert len(mock.request_history) == 2
    assert re.findall(r".*/project/PRJ", mock.request_history[0].url)
    assert re.findall(r".*/run/PRJ/3", mock.request_history[1].url)
    assert mock.request_history[0].headers.get("Token") == "45678"
