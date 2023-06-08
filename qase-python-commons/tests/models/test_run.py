from mock import Mock
import json
import time

from qaseio.commons.models.run import RunExecution, RunStats, Run

def test_run_execution():
    start_time = time.time()
    end_time = start_time + 1  # 1 second later
    execution = RunExecution(start_time, end_time)

    assert execution.start_time == start_time
    assert execution.end_time == end_time
    assert execution.duration == int((end_time - start_time) * 1000)
    assert execution.cumulative_duration == 0

    execution.track({"execution": {"duration": 1000}})
    assert execution.cumulative_duration == 1000

def test_run_stats():
    stats = RunStats()

    assert stats.passed == 0
    assert stats.failed == 0
    assert stats.skipped == 0
    assert stats.broken == 0
    assert stats.muted == 0
    assert stats.total == 0

    stats.track({"execution": {"status": "passed"}, "muted": False})
    assert stats.passed == 1
    assert stats.total == 1

    stats.track({"execution": {"status": "failed"}, "muted": True})
    assert stats.failed == 1
    assert stats.muted == 1
    assert stats.total == 2

def test_run():
    start_time = time.time()
    end_time = start_time + 1  # 1 second later
    run = Run(title="test_run", start_time=start_time, end_time=end_time)

    assert run.title == "test_run"
    assert isinstance(run.execution, RunExecution)
    assert isinstance(run.stats, RunStats)
    assert run.results == []
    assert run.threads == []
    assert run.environment == None

    result = {"id": 1, "title": "test_result", "execution": {"status": "passed", "duration": 1000, "thread": "thread1"}}
    run.add_result(result)
    assert len(run.results) == 1
    assert run.threads == ["thread1"]
    assert run.stats.passed == 1
    assert run.execution.cumulative_duration == 1000

    host_data = {"system": "Linux", "node": "test_node"}
    run.add_host_data(host_data)
    assert run.host_data == host_data

    json_str = run.to_json()
    assert isinstance(json.loads(json_str), dict)  # Ensure it's valid JSON and can be parsed