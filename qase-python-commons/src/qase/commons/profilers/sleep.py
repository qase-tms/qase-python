import time
import uuid

from functools import wraps

from ..models.runtime import Runtime
from ..models.step import Step, StepSleepData, StepType


class SleepProfiler:
    _original_sleep = None

    def __init__(self, runtime: Runtime, track_on_fail: bool = True):
        self.runtime = runtime
        self.track_on_fail = track_on_fail
        self.step = None

    def enable(self):
        if SleepProfiler._original_sleep is None:
            SleepProfiler._original_sleep = time.sleep
            time.sleep = self._sleep_wrapper(time.sleep)

    def disable(self):
        if SleepProfiler._original_sleep is not None:
            time.sleep = SleepProfiler._original_sleep
            SleepProfiler._original_sleep = None

    def _sleep_wrapper(self, func):
        @wraps(func)
        def wrapper(duration, *args, **kwargs):
            self._log_pre_sleep(duration)
            func(duration, *args, **kwargs)
            self._log_post_sleep()

        return wrapper

    def _log_pre_sleep(self, duration):
        # Log or track the pre-sleep call
        self.step = Step(
            id=str(uuid.uuid4()),
            step_type=StepType.SLEEP,
            data=StepSleepData(duration=duration)
        )
        # Assuming runtime can start a step without a request/response
        self.runtime.add_step(self.step)

    def _log_post_sleep(self):
        # Log or track the post-sleep call
        # Update the step status to passed as sleep doesn't fail like network calls
        self.runtime.finish_step(
            id=self.step.id,
            status='passed',
        )
        self.step = None
