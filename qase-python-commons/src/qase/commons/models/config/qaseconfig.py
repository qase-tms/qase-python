from enum import Enum
from typing import List

from .framework import Framework
from .report import ReportConfig
from .testops import TestopsConfig
from ..basemodel import BaseModel
from ... import QaseUtils


class Mode(Enum):
    testops = "testops"
    report = "report"
    off = "off"


class ExecutionPlan(BaseModel):
    path: str = None

    def __init__(self):
        self.path = "./build/qase-execution-plan.json"

    def set_path(self, path: str):
        self.path = path


class QaseConfig(BaseModel):
    mode: Mode = None
    fallback: Mode = None
    environment: str = None
    root_suite: str = None
    debug: bool = None
    execution_plan: ExecutionPlan = None
    testops: TestopsConfig = None
    report: ReportConfig = None
    profilers: list = None
    framework: Framework = None
    exclude_params: list = None

    def __init__(self):
        self.mode = Mode.off
        self.fallback = Mode.off
        self.debug = False
        self.testops = TestopsConfig()
        self.report = ReportConfig()
        self.execution_plan = ExecutionPlan()
        self.framework = Framework()
        self.profilers = []
        self.exclude_params = []

    def set_mode(self, mode: str):
        if any(mode == e.value for e in Mode.__members__.values()):
            self.mode = Mode[mode]

    def set_fallback(self, fallback: str):
        if any(fallback == e.value for e in Mode.__members__.values()):
            self.fallback = Mode[fallback]

    def set_environment(self, environment: str):
        self.environment = environment

    def set_profilers(self, profilers: list):
        self.profilers = profilers

    def set_root_suite(self, root_suite: str):
        self.root_suite = root_suite

    def set_debug(self, debug):
        self.debug = QaseUtils.parse_bool(debug)

    def set_exclude_params(self, exclude_params: List[str]):
        self.exclude_params = exclude_params
