from ..models.runtime import Runtime


class DbProfiler:
    _instance = None

    def __init__(self, runtime: Runtime, track_on_fail: bool = True):
        self._original_functions = {}
        self.runtime = runtime
        self.track_on_fail = track_on_fail
        self.step = None

    def enable(self):
        # TBD
        return

    def disable(self):
        # TBD
        return
