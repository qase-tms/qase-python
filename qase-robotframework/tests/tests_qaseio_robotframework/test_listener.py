import os

import pytest

@pytest.fixture
def setup_env():
    os.environ.setdefault("QASE_TO_API_TOKEN", "123")
    os.environ.setdefault("QASE_TO_PROJECT", "123")
    yield
    os.environ.pop("QASE_TO_API_TOKEN")
    os.environ.pop("QASE_TO_PROJECT")


def test_init_listener(setup_env):
    # Rewrite this test to use the listener
    assert True