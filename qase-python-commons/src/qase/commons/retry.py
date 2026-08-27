"""Bounded retry for result uploads.

Retries transport failures and the HTTP statuses that can succeed on a second
attempt. Never retries a status that would be rejected identically -- an
oversized batch, an invalid payload, an expired token -- where retrying only
delays the error and adds load.

Safe only because ResultCreate.id is populated: a request that was accepted
but whose response was lost is indistinguishable from one that never arrived,
and the idempotency key is what stops the retry creating duplicates.
"""

import time
from typing import Callable, Optional

RETRYABLE_STATUSES = frozenset({408, 429, 500, 502, 503, 504})

_TRANSPORT_ERRORS = (ConnectionError, OSError, TimeoutError)


def _urllib3_errors():
    try:
        from urllib3.exceptions import HTTPError

        return (HTTPError,)
    except ImportError:  # pragma: no cover - urllib3 is a hard dependency
        return ()


def is_retryable(exc: BaseException) -> bool:
    """True when another attempt could plausibly succeed."""
    status = getattr(exc, "status", None)
    if status is not None:
        try:
            return int(status) in RETRYABLE_STATUSES
        except (TypeError, ValueError):
            return False
    return isinstance(exc, _TRANSPORT_ERRORS + _urllib3_errors())


def retry_after_seconds(exc: BaseException) -> Optional[float]:
    """Seconds requested by a Retry-After header, when there is one.

    Qase answers 429 with roughly 60 seconds, which no short backoff ladder
    survives, so honouring the header matters more than the ladder itself.
    """
    headers = getattr(exc, "headers", None)
    if not headers:
        return None
    try:
        value = headers.get("Retry-After")
    except AttributeError:
        return None
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        # The RFC also allows an HTTP-date. We do not parse it: falling back to
        # the computed backoff is safer than guessing at a clock skew.
        return None


def send_with_retry(
    send: Callable[[], None],
    attempts: int,
    backoff: int,
    sleep: Callable[[float], None] = time.sleep,
    logger=None,
) -> None:
    """Call send(), retrying retryable failures. Re-raises the last exception.

    `attempts` is the total number of tries, not the number of retries on top
    of the first: a configured `retries: 3` means three attempts in all, and
    `retries: 0` still sends once but never retries.
    """
    attempts = max(1, attempts)
    for attempt in range(1, attempts + 1):
        try:
            send()
            return
        except Exception as exc:
            if attempt == attempts or not is_retryable(exc):
                raise
            delay = retry_after_seconds(exc)
            if delay is None:
                delay = backoff ** attempt
            if logger:
                logger.log(
                    f"Upload attempt {attempt}/{attempts} failed ({exc}); "
                    f"retrying in {delay}s",
                    "warning",
                )
            sleep(delay)
