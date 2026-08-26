import pytest

from qase.commons.retry import is_retryable, retry_after_seconds, send_with_retry


class FakeApiException(Exception):
    """Shaped like the generated client's ApiException: .status and .headers."""

    def __init__(self, status, headers=None):
        super().__init__(f"status {status}")
        self.status = status
        self.headers = headers or {}


@pytest.mark.parametrize("status", [408, 429, 500, 502, 503, 504])
def test_retryable_statuses(status):
    assert is_retryable(FakeApiException(status)) is True


@pytest.mark.parametrize("status", [400, 401, 403, 404, 413, 422, 507])
def test_non_retryable_statuses(status):
    assert is_retryable(FakeApiException(status)) is False


def test_transport_errors_are_retryable():
    assert is_retryable(ConnectionResetError(104, "Connection reset by peer")) is True
    assert is_retryable(OSError("network unreachable")) is True


def test_unknown_exceptions_are_not_retryable():
    assert is_retryable(ValueError("bad payload")) is False


def test_retry_after_is_read_from_headers():
    assert retry_after_seconds(FakeApiException(429, {"Retry-After": "60"})) == 60.0


def test_retry_after_absent_or_unparsable():
    assert retry_after_seconds(FakeApiException(429)) is None
    assert retry_after_seconds(FakeApiException(429, {"Retry-After": "soon"})) is None
    assert retry_after_seconds(ConnectionResetError()) is None


def test_succeeds_without_retrying():
    calls = []
    send_with_retry(lambda: calls.append(1), attempts=3, backoff=2, sleep=lambda s: None)
    assert len(calls) == 1


def test_retries_until_success_with_exponential_backoff():
    calls = []
    slept = []

    def send():
        calls.append(1)
        if len(calls) < 3:
            raise ConnectionResetError()

    send_with_retry(send, attempts=3, backoff=2, sleep=slept.append)
    assert len(calls) == 3
    assert slept == [2, 4]


def test_gives_up_and_reraises_after_exhausting_attempts():
    calls = []

    def send():
        calls.append(1)
        raise ConnectionResetError()

    with pytest.raises(ConnectionResetError):
        send_with_retry(send, attempts=3, backoff=2, sleep=lambda s: None)
    assert len(calls) == 3


def test_does_not_retry_a_non_retryable_error():
    calls = []

    def send():
        calls.append(1)
        raise FakeApiException(413)

    with pytest.raises(FakeApiException):
        send_with_retry(send, attempts=3, backoff=2, sleep=lambda s: None)
    assert len(calls) == 1


def test_retry_after_overrides_backoff():
    calls = []
    slept = []

    def send():
        calls.append(1)
        if len(calls) < 2:
            raise FakeApiException(429, {"Retry-After": "60"})

    send_with_retry(send, attempts=3, backoff=2, sleep=slept.append)
    assert slept == [60.0]


def test_attempts_of_one_means_no_retry():
    calls = []

    def send():
        calls.append(1)
        raise ConnectionResetError()

    with pytest.raises(ConnectionResetError):
        send_with_retry(send, attempts=1, backoff=2, sleep=lambda s: None)
    assert len(calls) == 1


def test_zero_attempts_still_tries_once():
    """retries: 0 in config means "do not retry", not "do not send"."""
    calls = []
    send_with_retry(lambda: calls.append(1), attempts=0, backoff=2, sleep=lambda s: None)
    assert len(calls) == 1
