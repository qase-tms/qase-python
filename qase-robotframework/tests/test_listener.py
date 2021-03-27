import os

import pytest

from qaseio.robotframework import Listener


@pytest.fixture
def setup_env():
    os.environ.setdefault("QASE_API_TOKEN", "123")
    os.environ.setdefault("QASE_PROJECT", "123")
    yield
    os.environ.pop("QASE_API_TOKEN")
    os.environ.pop("QASE_PROJECT")


def test_init_listener(setup_env):
    Listener()


def test_init_listener_error():
    with pytest.raises(ValueError):
        Listener()
