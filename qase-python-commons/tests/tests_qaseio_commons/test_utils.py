from mock import Mock
import os
import threading
import sys
import pip

from qaseio.commons import QaseUtils

def test_build_tree():
    # Mocking item objects
    item1 = Mock()
    item1.id = 1
    item1.parent_id = None
    item1.steps = []

    item2 = Mock()
    item2.id = 2
    item2.parent_id = 1
    item2.steps = []

    items = [item1, item2]

    roots = QaseUtils.build_tree(items)
    assert len(roots) == 1
    assert roots[0] is item1
    assert roots[0].steps[0] is item2

def test_get_thread_name():
    thread_name = QaseUtils.get_thread_name()
    assert thread_name == f"{os.getpid()}-{threading.current_thread().name}"

def test_get_host_data():
    host_data = QaseUtils.get_host_data()

    assert host_data['system'] == os.uname().sysname
    assert host_data['node'] == os.uname().nodename
    assert host_data['release'] == os.uname().release
    assert host_data['version'] == os.uname().version
    assert host_data['machine'] == os.uname().machine
    assert host_data['python'] == '.'.join(map(str, sys.version_info))
    assert host_data['pip'] == pip.__version__

def test_get_filename():
    path = '/path/to/file.txt'
    filename = QaseUtils.get_filename(path)
    assert filename == 'file.txt'