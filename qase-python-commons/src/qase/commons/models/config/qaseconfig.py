from enum import Enum
from typing import List, Dict, Optional

from .framework import Framework
from .report import ReportConfig
from .testops import TestopsConfig, TestopsMultiConfig
from ..basemodel import BaseModel
from ... import QaseUtils


class Mode(Enum):
    testops = "testops"
    testops_multi = "testops_multi"
    report = "report"
    off = "off"


class LoggingConfig(BaseModel):
    console: Optional[bool] = None
    file: Optional[bool] = None

    def __init__(self):
        self.console = None
        self.file = None

    def set_console(self, console: bool):
        self.console = console

    def set_file(self, file: bool):
        self.file = file


class ExecutionPlan(BaseModel):
    path: str = None

    def __init__(self):
        self.path = "./build/qase-execution-plan.json"

    def set_path(self, path: str):
        self.path = path


class NetworkProfilerConfig(BaseModel):
    exclude_hosts: List[str] = None

    def __init__(self):
        self.exclude_hosts = []

    def set_exclude_hosts(self, hosts: List[str]):
        self.exclude_hosts = hosts


class QaseConfig(BaseModel):
    mode: Mode = None
    fallback: Mode = None
    environment: str = None
    root_suite: str = None
    debug: bool = None
    execution_plan: ExecutionPlan = None
    testops: TestopsConfig = None
    testops_multi: TestopsMultiConfig = None
    report: ReportConfig = None
    profilers: list = None
    network_profiler: NetworkProfilerConfig = None
    framework: Framework = None
    exclude_params: list = None
    status_mapping: Dict[str, str] = None
    logging: LoggingConfig = None

    def __init__(self):
        self.mode = Mode.off
        self.fallback = Mode.off
        self.debug = False
        self.testops = TestopsConfig()
        self.testops_multi = TestopsMultiConfig()
        self.report = ReportConfig()
        self.execution_plan = ExecutionPlan()
        self.framework = Framework()
        self.profilers = []
        self.network_profiler = NetworkProfilerConfig()
        self.exclude_params = []
        self.status_mapping = {}
        self.logging = LoggingConfig()

    def set_mode(self, mode: str):
        if any(mode == e.value for e in Mode.__members__.values()):
            self.mode = Mode[mode]

    def set_fallback(self, fallback: str):
        if any(fallback == e.value for e in Mode.__members__.values()):
            self.fallback = Mode[fallback]

    def set_environment(self, environment: str):
        self.environment = environment

    def set_profilers(self, profilers: list):
        self.profilers = []
        for item in profilers:
            if isinstance(item, str):
                self.profilers.append(item)
            elif isinstance(item, dict):
                name = item.get("name")
                if name:
                    self.profilers.append(name)
                    if name == "network" and "excludeHosts" in item:
                        self.network_profiler.set_exclude_hosts(item["excludeHosts"])

    def set_root_suite(self, root_suite: str):
        self.root_suite = root_suite

    def set_debug(self, debug):
        self.debug = QaseUtils.parse_bool(debug)

    def set_exclude_params(self, exclude_params: List[str]):
        self.exclude_params = exclude_params

    def set_status_mapping(self, status_mapping: Dict[str, str]):
        self.status_mapping = status_mapping

    def set_logging(self, logging_config: dict):
        if logging_config.get("console") is not None:
            self.logging.set_console(QaseUtils.parse_bool(logging_config.get("console")))
        if logging_config.get("file") is not None:
            self.logging.set_file(QaseUtils.parse_bool(logging_config.get("file")))

    def set_testops_multi(self, testops_multi_config: dict):
        """Set testops multi configuration from dictionary"""
        if testops_multi_config:
            if 'default_project' in testops_multi_config:
                self.testops_multi.set_default_project(testops_multi_config['default_project'])
            if 'projects' in testops_multi_config:
                from .testops import ProjectConfig
                projects = []
                for project_data in testops_multi_config['projects']:
                    project = ProjectConfig()
                    if 'code' in project_data:
                        project.set_code(project_data['code'])
                    if 'run' in project_data:
                        project.set_run(project_data['run'])
                    if 'plan' in project_data:
                        project.set_plan(project_data['plan'])
                    if 'environment' in project_data:
                        project.set_environment(project_data['environment'])
                    projects.append(project)
                self.testops_multi.set_projects(projects)
