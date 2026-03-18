from mock import Mock
import os
import threading
import time

from qase.commons.utils import QaseUtils

try:
    from freezegun import freeze_time
    FREEZEGUN_AVAILABLE = True
except ImportError:
    FREEZEGUN_AVAILABLE = False

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

def test_get_filename():
    path = '/path/to/file.txt'
    filename = QaseUtils.get_filename(path)
    assert filename == 'file.txt'

def test_get_real_time():
    """Test that get_real_time() returns current time"""
    before = time.time()
    real_time = QaseUtils.get_real_time()
    after = time.time()
    
    # The real time should be between before and after
    assert before <= real_time <= after

def test_get_real_time_with_freezegun():
    """Test that get_real_time() returns real time even when freezegun is active"""
    if not FREEZEGUN_AVAILABLE:
        # Skip test if freezegun is not installed
        return
    
    # Get current time before freezing
    real_time_before = time.time()
    
    # Freeze time to a date in the past (2023-02-01)
    with freeze_time("2023-02-01"):
        # time.time() should return the frozen time
        frozen_time = time.time()
        
        # get_real_time() should return the real current time
        real_time = QaseUtils.get_real_time()
        
        # The frozen time should be much earlier than real time
        # 2023-02-01 timestamp is around 1675209600
        assert frozen_time < 1700000000, f"Expected frozen time to be in the past, got {frozen_time}"
        
        # Real time should be close to current time (not frozen)
        assert real_time > real_time_before, f"Expected real time {real_time} to be >= {real_time_before}"
        
        # Real time should be significantly greater than frozen time
        assert real_time > frozen_time + 60000000, f"Expected real time {real_time} to be much greater than frozen time {frozen_time}"
