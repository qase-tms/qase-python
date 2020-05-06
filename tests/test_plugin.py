import re

import pytest

from qaseio.pytest.plugin import get_ids_from_pytest_nodes

PYTEST_FILE = """
from qaseio.pytest import qase

def test_no_deco():
    pass

@qase.id(4)
def test_single_id():
    pass

@qase.id(5, 7)
def test_multiple_ids():
    pass
"""


@pytest.fixture()
def testfile(testdir):
    testdir.makepyfile(PYTEST_FILE)
    return testdir.getitems(PYTEST_FILE)


def test_get_ids_from_pytest_nodes(testfile):
    print(testfile)
    data, ids = get_ids_from_pytest_nodes(testfile)
    assert len(data) == 2
    assert len(ids) == 1
    assert data[testfile[1].nodeid].get("ids") == (4,)
    assert data[testfile[2].nodeid].get("ids") == (5, 7)


def test_plugin_init(qs_plugin, mock):
    qs_plugin()
    assert len(mock.request_history) == 2
    assert re.findall(r".*/project/[a-zA-Z]+", mock.request_history[0].url)
    assert re.findall(r".*/run/[a-zA-Z]+/\w+", mock.request_history[1].url)


def test_pytest_report_header(qs_plugin, mock):
    plugin = qs_plugin()
    text = plugin.pytest_report_header(None, None)
    assert text == "qase: existing testrun #123 selected"
    plugin.testrun_id = None
    text = plugin.pytest_report_header(None, None)
    assert text == "qase: a new testrun will be created"
