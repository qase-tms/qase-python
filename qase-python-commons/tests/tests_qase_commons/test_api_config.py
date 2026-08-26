import pytest

from qase.commons.models.config.api import ApiConfig


def test_defaults():
    config = ApiConfig()
    assert config.timeout == 30
    assert config.retries == 3
    assert config.retry_backoff == 2


def test_setters():
    config = ApiConfig()
    config.set_timeout(5)
    config.set_retries(0)
    config.set_retry_backoff(1)
    assert (config.timeout, config.retries, config.retry_backoff) == (5, 0, 1)


def test_setters_accept_strings_from_environment_variables():
    config = ApiConfig()
    config.set_timeout("5")
    config.set_retries("0")
    config.set_retry_backoff("1")
    assert (config.timeout, config.retries, config.retry_backoff) == (5, 0, 1)


def test_timeout_must_be_positive():
    with pytest.raises(ValueError):
        ApiConfig().set_timeout(0)


def test_retries_cannot_be_negative():
    with pytest.raises(ValueError):
        ApiConfig().set_retries(-1)


def test_retry_backoff_cannot_be_negative():
    with pytest.raises(ValueError):
        ApiConfig().set_retry_backoff(-1)
