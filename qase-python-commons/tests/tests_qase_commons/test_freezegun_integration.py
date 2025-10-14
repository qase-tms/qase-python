"""
Integration tests for freezegun compatibility.

These tests verify that Qase reporters work correctly when tests use freezegun
to mock time. The issue is that freezegun mocks time.time(), which affects
execution timestamps, but Qase API requires real timestamps.
"""

import time
import pytest

try:
    from freezegun import freeze_time
    FREEZEGUN_AVAILABLE = True
except ImportError:
    FREEZEGUN_AVAILABLE = False

from qase.commons.models.result import Execution, Result
from qase.commons.models.step import Step, StepType, StepTextData


@pytest.mark.skipif(not FREEZEGUN_AVAILABLE, reason="freezegun not installed")
class TestFreezegunIntegration:
    """Test that Qase works correctly with freezegun"""
    
    def test_execution_timestamps_with_freezegun(self):
        """
        Test that Execution timestamps are real time even when freezegun is active.
        
        This reproduces the issue from GitHub issue #415 where users get
        "Data is invalid" errors when using freezegun with Qase steps.
        """
        # Get current real time
        real_time_before = time.time()
        
        # Freeze time to 2023-02-01
        with freeze_time("2023-02-01"):
            # time.time() returns frozen time
            frozen_time = time.time()
            assert frozen_time < 1700000000, "Time should be frozen in the past"
            
            # Create execution (this is what happens when test starts)
            execution = Execution()
            
            # Small delay to ensure end_time > start_time
            time.sleep(0.1)  # This is also mocked by freezegun
            
            # Complete execution
            execution.complete()
            
            # Verify that execution times are real (not frozen)
            # They should be close to current time, not 2023-02-01
            assert execution.start_time > frozen_time + 60000000, \
                f"start_time {execution.start_time} should be real time, not frozen time {frozen_time}"
            
            assert execution.end_time > frozen_time + 60000000, \
                f"end_time {execution.end_time} should be real time, not frozen time {frozen_time}"
            
            assert execution.start_time >= real_time_before, \
                f"start_time {execution.start_time} should be >= {real_time_before}"
            
            # Duration should be positive
            assert execution.duration >= 0, \
                f"duration {execution.duration} should be non-negative"
            
            # Verify timestamps would be accepted by Qase API
            # (API requires timestamps >= current time - some tolerance)
            current_timestamp = 1760383058  # Example from error message
            # Our timestamps should be much greater than this example from Oct 2025
            # Since we're running tests later
            assert execution.start_time > 1700000000, \
                f"Timestamp {execution.start_time} should be valid for Qase API"
    
    def test_step_execution_with_freezegun(self):
        """
        Test that Step execution timestamps are real time when freezegun is active.
        """
        real_time_before = time.time()
        
        with freeze_time("2023-02-01"):
            frozen_time = time.time()
            
            # Create a step (this is what happens with qase.step())
            step = Step(
                step_type=StepType.TEXT,
                id="test-step-1",
                data=StepTextData(action="Test action")
            )
            
            # Simulate some work
            time.sleep(0.01)
            
            # Complete the step
            step.execution.complete()
            
            # Verify timestamps are real
            assert step.execution.start_time > frozen_time + 60000000, \
                "step start_time should be real time"
            
            assert step.execution.end_time > frozen_time + 60000000, \
                "step end_time should be real time"
            
            assert step.execution.start_time >= real_time_before, \
                "step start_time should be >= real time before test"
            
            assert step.execution.duration >= 0, \
                "step duration should be non-negative"
    
    def test_result_with_steps_freezegun(self):
        """
        Test complete Result with steps when freezegun is active.
        
        This simulates the exact scenario from the user's issue.
        """
        with freeze_time("2023-02-01"):
            frozen_time = time.time()
            
            # Create result
            result = Result(title="Test with freezegun", signature="test-sig")
            
            # Simulate test execution with step
            step = Step(
                step_type=StepType.TEXT,
                id="step-1",
                data=StepTextData(action="Doing something")
            )
            
            time.sleep(0.01)
            step.execution.complete()
            
            result.steps.append(step)
            result.execution.set_status("passed")
            result.execution.complete()
            
            # Verify all timestamps are real (not frozen)
            assert result.execution.start_time > frozen_time + 60000000, \
                "result start_time should not be frozen"
            
            assert result.execution.end_time > frozen_time + 60000000, \
                "result end_time should not be frozen"
            
            assert step.execution.start_time > frozen_time + 60000000, \
                "step start_time should not be frozen"
            
            assert step.execution.end_time > frozen_time + 60000000, \
                "step end_time should not be frozen"
            
            # All durations should be valid
            assert result.execution.duration >= 0
            assert step.execution.duration >= 0
    
    def test_multiple_freezegun_contexts(self):
        """
        Test that timestamps work correctly across multiple freezegun contexts.
        """
        executions = []
        
        # First frozen context
        with freeze_time("2023-01-01"):
            exec1 = Execution()
            time.sleep(0.01)
            exec1.complete()
            executions.append(exec1)
        
        # Second frozen context (different time)
        with freeze_time("2023-06-01"):
            exec2 = Execution()
            time.sleep(0.01)
            exec2.complete()
            executions.append(exec2)
        
        # Outside frozen context
        exec3 = Execution()
        time.sleep(0.01)
        exec3.complete()
        executions.append(exec3)
        
        # All executions should have real timestamps
        # and should be close to each other (not separated by months)
        for i, exec in enumerate(executions):
            assert exec.start_time > 1700000000, \
                f"Execution {i} should have real timestamp"
            assert exec.duration >= 0, \
                f"Execution {i} should have valid duration"
        
        # Timestamps should be sequential (each one after the previous)
        for i in range(len(executions) - 1):
            assert executions[i].end_time <= executions[i + 1].start_time + 1, \
                f"Execution {i+1} should start after execution {i} ends"

