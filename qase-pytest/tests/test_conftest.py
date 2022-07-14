import re
import json
from unittest.mock import MagicMock, patch

TEST_FILE = """
from src.pytest import qase
@qase.id(1)
def test_example():
    pass
"""

project = "PRJ"
run_id = 3
case_id = 1

calls = []


def get_data(method, url):
    if method == 'GET' and url.find(f'/v1/project/{project}'):
        return {
            'status': True,
            'result': {'code': project},
        }


def make_response(method, url, *args, **kwargs):
    # Log a fake request for test output purposes
    global calls
    calls.append({
        'method': method,
        'url': url,
        'headers': kwargs['headers']
    })
    # Create a new Mock to imitate a Response
    response_mock = MagicMock()
    response_mock.status = 200
    response_mock.data = json.dumps(get_data(method, url))
    return response_mock


@patch('urllib3.PoolManager')
def test_run_all_parameters_cli(mock_pm, testdir):
    global calls
    calls = []
    mock_instance = mock_pm.return_value
    mock_instance.request.side_effect = make_response
    testdir.makepyfile(
        """
    from qaseio.pytest import qase
    @qase.id(1)
    def test_example():
        pass
    """
    )
    result = testdir.runpytest(
        "--qase",
        "--qase-project=PRJ",
        "--qase-new-run",
        "--qase-api-token=12345",
        "--qase-debug",
    )
    assert len(calls) == 1
    assert re.findall(r".*/project/PRJ", calls[0]['url'])
    assert calls[0]['headers'].get("Token") == "12345"
