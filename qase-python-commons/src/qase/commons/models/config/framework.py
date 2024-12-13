from enum import Enum
from typing import Type, Union

from ..basemodel import BaseModel
from ... import QaseUtils


class Video(Enum):
    off = "off"
    on = "on"
    failed = "retain-on-failure"


class Trace(Enum):
    off = "off"
    on = "on"
    failed = "retain-on-failure"


class XFailStatus(BaseModel):
    xfail: str = None
    xpass: str = None

    def __init__(self):
        self.xfail = 'skipped'
        self.xpass = 'passed'

    def set_xfail(self, value: str):
        self.xfail = value

    def set_xpass(self, value: str):
        self.xpass = value


class PytestConfig(BaseModel):
    capture_logs: bool = None
    xfail_status: XFailStatus = None

    def __init__(self):
        self.capture_logs = False
        self.xfail_status = XFailStatus()

    def set_capture_logs(self, capture_logs):
        self.capture_logs = QaseUtils.parse_bool(capture_logs)


class PlaywrightConfig(BaseModel):
    output_dir: str = None
    video: Video = None
    trace: Trace = None

    def __init__(self):
        self.output_dir = "test-results"
        self.video = Video.off
        self.trace = Trace.off

    def set_output_dir(self, output_dir: str):
        self.output_dir = output_dir

    def set_video(self, value: str):
        self.video = self.__set_mode(Video, value)

    def set_trace(self, value: str):
        self.trace = self.__set_mode(Trace, value)

    @staticmethod
    def __set_mode(enum_class: Type[Union[Video, Trace]], value: str):
        for mode in enum_class:
            if mode.value == value:
                return mode
        return None


class Framework(BaseModel):
    pytest: PytestConfig = None
    playwright: PlaywrightConfig = None

    def __init__(self):
        self.pytest = PytestConfig()
        self.playwright = PlaywrightConfig()
