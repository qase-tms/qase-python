from ..basemodel import BaseModel
from ... import QaseUtils


class PytestConfig(BaseModel):
    capture_logs: bool = None

    def __init__(self):
        self.capture_logs = False

    def set_capture_logs(self, capture_logs):
        self.capture_logs = QaseUtils.parse_bool(capture_logs)


class Framework(BaseModel):
    pytest: PytestConfig = None

    def __init__(self):
        self.pytest = PytestConfig()
