from ..basemodel import BaseModel


class PytestConfig(BaseModel):
    capture_logs: bool = None

    def __init__(self):
        self.capture_logs = False

    def set_capture_logs(self, capture_logs: bool):
        self.capture_logs = capture_logs


class Framework(BaseModel):
    pytest: PytestConfig = None

    def __init__(self):
        self.pytest = PytestConfig()
