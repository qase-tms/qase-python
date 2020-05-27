import json
import re
from enum import Enum

import pytest

from qaseio.client.models import TestRunResultStatus
from qaseio.pytest.plugin import QasePytestPlugin, get_ids_from_pytest_nodes

PYTEST_FILE = """
from qaseio.pytest import qase

def test_no_deco():
    pass

@qase.id(1)
def test_single_id():
    pass

@qase.id(2, 3)
def test_multiple_ids():
    pass
"""

PYTEST_ALL_DECOS_FILE = """
from qaseio.pytest import qase

@qase.id(1)
def test_single_id():
    pass

@qase.id(4, 3)
def test_multiple_ids():
    pass
"""

PYTEST_COMPLEX_FILE = """
import pytest
from qaseio.pytest import qase

def test_no_deco():
    pass

@qase.id(1)
def test_single_id_fail():
    assert 0

@qase.id(2, 3)
def test_multiple_ids_fail():
    assert 0

@qase.id(4)
def test_single_id_pass():
    pass

@qase.id(5, 6)
def test_multiple_ids_pass():
    pass

@pytest.fixture(scope="session")
def setup():
    raise ValueError()

@qase.id(7)
def test_single_id_setup_fail(setup):
    pass

@qase.id(8, 9)
def test_multiple_ids_setup_fail(setup):
    pass

@pytest.fixture()
def teardown():
    yield
    raise ValueError()

@qase.id(10)
def test_single_id_teardown_fail(teardown):
    pass

@qase.id(11, 12)
def test_multiple_ids_teardown_fail(teardown):
    pass

@qase.id(13)
@pytest.mark.skip
def test_single_id_teardown_skip():
    pass

@qase.id(14, 15)
@pytest.mark.skip
def test_multiple_ids_teardown_skip():
    pass
"""


class FakeTerminalWriter:
    results = []

    def ensure_newline(self):
        pass

    def section(self, *args, **kwargs):
        pass

    def line(self, s="", **kw):
        self.results.append([s, kw])


class FakePluginManager:
    writer = None

    def set_writer(self, writer):
        self.writer = writer

    def get_plugin(self, *args, **kwargs):
        return self.writer


class FakeConf:
    pluginmanager = FakePluginManager()


@pytest.fixture()
def testfile(testdir):
    testdir.makepyfile(PYTEST_FILE)
    return testdir.getitems(PYTEST_FILE)


def test_get_ids_from_pytest_nodes(testfile):
    print(testfile)
    data, ids = get_ids_from_pytest_nodes(testfile)
    assert len(data) == 2
    assert len(ids) == 1
    assert data[testfile[1].nodeid].get("ids") == (1,)
    assert data[testfile[2].nodeid].get("ids") == (2, 3)


def test_plugin_init(qs_plugin, mock):
    qs_plugin()
    assert len(mock.request_history) == 2
    assert re.findall(r".*/project/[a-zA-Z]+", mock.request_history[0].url)
    assert re.findall(r".*/run/[a-zA-Z]+/\w+", mock.request_history[1].url)


def test_plugin_init_missing_project(mock):
    mock.get("/v1/project/123", status_code=404)
    with pytest.raises(ValueError):
        QasePytestPlugin("123", "123", None)


def test_plugin_init_missing_run_id(mock, default_mocks):
    default_mocks()
    mock.get("/v1/run/PRJ/123123", status_code=404)
    with pytest.raises(ValueError):
        QasePytestPlugin("123", "PRJ", 123123)


def test_pytest_report_header(qs_plugin, mock):
    plugin = qs_plugin()
    text = plugin.pytest_report_header(None, None)
    assert text == "qase: existing testrun #123 selected"
    plugin.testrun_id = None
    text = plugin.pytest_report_header(None, None)
    assert text == "qase: a new testrun will be created"


def test_pytest_collection_modifyitems(qs_plugin, mock, cases_mocks, testfile):
    cases_mocks()
    config = FakeConf()
    writer = FakeTerminalWriter()
    config.pluginmanager.set_writer(writer)
    plugin = qs_plugin(debug=True)
    mock.reset_mock()
    plugin.pytest_collection_modifyitems(None, config, testfile)
    assert len(mock.request_history) == 3
    assert len(writer.results) == 2
    assert len(plugin.nodes_with_ids) == 2


@pytest.mark.parametrize(
    "cases_kwargs, tests",
    [({"status_code": 404}, PYTEST_FILE), ({}, PYTEST_ALL_DECOS_FILE)],
)
def test_pytest_collection_modifyitems_missing_cases(
    qs_plugin, mock, cases_mocks, testdir, cases_kwargs, tests
):
    cases_mocks(**cases_kwargs)
    plugin = qs_plugin()
    mock.reset_mock()
    testdir.makepyfile(tests)
    items = testdir.getitems(tests)
    plugin.pytest_collection_modifyitems(None, None, items)
    assert len(mock.request_history) == 3
    assert len(plugin.nodes_with_ids) == 2


def test_start_pytest_item(qs_plugin, mock, cases_mocks, testfile):
    cases_mocks()
    plugin = qs_plugin()
    mock.reset_mock()
    plugin.pytest_collection_modifyitems(None, None, testfile)
    mock.reset_mock()
    mock.post(
        "/v1/result/PRJCODE/123",
        json={"status": True, "result": {"hash": "1a2b3d"}},
    )
    for item in testfile:
        plugin.start_pytest_item(item)
    assert len(mock.request_history) == 2
    for k, v in plugin.nodes_with_ids.items():
        assert v.get("hashes") == ["1a2b3d"]


@pytest.fixture
def start_items(qs_plugin, mock, cases_mocks, testfile):
    cases_mocks()
    plugin = qs_plugin()
    plugin.pytest_collection_modifyitems(None, None, testfile)
    mock.post(
        "/v1/result/PRJCODE/123",
        json={"status": True, "result": {"hash": "1a2b3d"}},
    )
    for item in testfile:
        plugin.start_pytest_item(item)
    mock.reset_mock()
    return plugin


def test_finish_pytest_item_no_errors(mock, start_items, testfile):
    plugin = start_items
    mock.patch(
        "/v1/result/PRJCODE/123/1a2b3d",
        json={"status": True, "result": {"hash": "1a2b3d"}},
    )
    for k, v in plugin.nodes_with_ids.items():
        v["result"] = TestRunResultStatus.PASSED
    for item in testfile:
        plugin.finish_pytest_item(item)
    assert len(mock.request_history) == 2
    for req in mock.request_history:
        data = json.loads(req.body)
        assert data.get("status") == "passed"
        assert data.get("comment") == plugin.comment


def test_finish_pytest_item_errors(mock, start_items, testfile):
    plugin = start_items
    mock.patch(
        "/v1/result/PRJCODE/123/1a2b3d",
        json={"status": True, "result": {"hash": "1a2b3d"}},
    )
    for k, v in plugin.nodes_with_ids.items():
        v["result"] = TestRunResultStatus.FAILED
        v["error"] = "error"
    for item in testfile:
        plugin.finish_pytest_item(item)
    assert len(mock.request_history) == 2
    for req in mock.request_history:
        data = json.loads(req.body)
        assert data.get("status") == "failed"
        assert data.get("comment") == plugin.comment
        assert data.get("stacktrace") == "error"
        assert data.get("time") is not None


def test_complex_run(qs_plugin, mock, default_mocks, cases_mocks, testdir):
    default_mocks()
    cases_mocks()

    def json_callback(request, context):
        data = json.loads(request.body)
        return {"status": True, "result": {"hash": str(data.get("case_id"))}}

    result = {"status": True, "result": {"hash": "1a2b3d"}}
    mock.post("/v1/result/PRJ/3", json=json_callback)
    mock.patch(re.compile(r"/v1/result/PRJ/3/[0-9]+"), json=result)
    testdir.makepyfile(PYTEST_COMPLEX_FILE)
    items = testdir.getitems(PYTEST_COMPLEX_FILE)
    testdir.runpytest(
        "-v",
        "--qase",
        "--qase-project=PRJ",
        "--qase-testrun=3",
        "--qase-api-token=12345",
        "--qase-debug",
    )
    data, _ = get_ids_from_pytest_nodes(items)
    for nodeid, values in data.items():
        status = TestRunResultStatus.PASSED
        if ("setup" in nodeid or "teardown" in nodeid) and "fail" in nodeid:
            status = TestRunResultStatus.BLOCKED
        elif "skip" in nodeid:
            status = "skipped"
        elif "fail" in nodeid:
            status = TestRunResultStatus.FAILED
        print(nodeid, status)
        for _id in values.get("ids"):
            for req in mock.request_history:
                if req.url.endswith(f"result/PRJ/3/{_id}"):
                    data = json.loads(req.body)
                    if isinstance(status, Enum):
                        status = status.value
                    assert data.get("status") == status
