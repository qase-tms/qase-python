import threading
from unittest.mock import Mock

from qase.commons.models.result import Result
from qase.commons.reporters.testops import QaseTestOps


def _reporter(client, retries=1, backoff=0):
    """A QaseTestOps with __init__ bypassed, wired for the send path only.

    The real __init__ builds API clients and calls get_project, which needs a
    live server. Only the attributes the send and completion paths touch are
    set here.
    """
    reporter = QaseTestOps.__new__(QaseTestOps)
    reporter.config = Mock()
    reporter.config.testops.status_filter = []
    reporter.config.testops.api.retries = retries
    reporter.config.testops.api.retry_backoff = backoff
    reporter.config.testops.show_public_report_link = False
    reporter.logger = Mock()
    reporter.client = client
    reporter.project_code = "DEMO"
    reporter.run_id = 1
    reporter.results = []
    reporter.processed = []
    reporter.lost_results = 0
    reporter.lock = threading.Lock()
    reporter.send_semaphore = threading.Semaphore(4)
    reporter.count_running_threads = 0
    reporter.complete_after_run = True
    return reporter


def _results(count):
    return [Result(title=f"t{i}", signature=f"s{i}") for i in range(count)]


def test_successful_send_records_processed_and_loses_nothing():
    reporter = _reporter(Mock())
    reporter._send_results_threaded(_results(3))
    assert len(reporter.processed) == 3
    assert reporter.lost_results == 0


def test_exhausted_retries_count_the_batch_as_lost():
    client = Mock()
    client.send_results.side_effect = ConnectionResetError(104, "reset")
    reporter = _reporter(client, retries=2)
    reporter._send_results_threaded(_results(50))
    assert reporter.lost_results == 50
    assert reporter.processed == []


def test_a_retryable_failure_is_retried_then_succeeds():
    client = Mock()
    client.send_results.side_effect = [ConnectionResetError(), None]
    reporter = _reporter(client, retries=2)
    reporter._send_results_threaded(_results(2))
    assert client.send_results.call_count == 2
    assert reporter.lost_results == 0
    assert len(reporter.processed) == 2


def test_the_thread_no_longer_raises_out_of_the_worker():
    """The batch is accounted for instead of escaping as a thread exception.

    Re-raising here only ever produced a PytestUnhandledThreadExceptionWarning
    that nothing acted on, which is how the loss stayed silent.
    """
    client = Mock()
    client.send_results.side_effect = ConnectionResetError()
    reporter = _reporter(client, retries=1)
    reporter._send_results_threaded(_results(1))  # must not raise
    assert reporter.lost_results == 1


def test_the_worker_releases_its_slot_even_when_the_batch_is_lost():
    client = Mock()
    client.send_results.side_effect = ConnectionResetError()
    reporter = _reporter(client, retries=1)
    reporter.count_running_threads = 1
    reporter.send_semaphore.acquire()
    reporter._send_results_threaded(_results(1))
    assert reporter.count_running_threads == 0
    assert reporter.send_semaphore.acquire(blocking=False) is True


def test_complete_run_skips_completion_when_results_were_lost():
    client = Mock()
    reporter = _reporter(client)
    reporter.lost_results = 100
    reporter.complete_run()
    client.complete_run.assert_not_called()
    logged = " ".join(str(call) for call in reporter.logger.log.call_args_list)
    assert "100" in logged


def test_complete_run_completes_when_nothing_was_lost():
    client = Mock()
    reporter = _reporter(client)
    reporter.complete_run()
    client.complete_run.assert_called_once_with("DEMO", 1)
