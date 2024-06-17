import os
import json
import time

from ..config import ConfigManager
from ..logger import Logger

from .report import QaseReport
from .testops import QaseTestOps

from ..models import Result, Attachment, Runtime
from ..models.config.qaseconfig import Mode
from typing import Union

"""
    CoreReporter is a facade for all reporters and it is used to initialize and manage them.
    It is also used to pass configuration and logger to reporters, handle fallback logic and error handling.
"""


class QaseCoreReporter:
    def __init__(self, config: ConfigManager):
        config.validate_config()
        self.config = config.config
        self.logger = Logger(self.config.debug)
        self.execution_plan = None
        self.profilers = []
        self.overhead = 0

        # self._selective_execution_setup()
        self.fallback = self._fallback_setup()

        self.logger.log_debug(f"Config: {self.config}")

        # Reading reporter mode from config file
        mode = self.config.mode

        if mode == Mode.testops:
            try:
                self._load_testops_plan()
                self.reporter = QaseTestOps(config=self.config, logger=self.logger)
            except Exception as e:
                self.logger.log('Failed to initialize TestOps reporter. Using fallback.', 'info')
                self.logger.log(e, 'error')
                self.reporter = self.fallback
        elif mode == Mode.report:
            self.reporter = QaseReport(config=self.config, logger=self.logger)
        else:
            self.reporter = None

    def start_run(self) -> Union[str, None]:
        if self.reporter:
            try:
                ts = time.time()
                self.logger.log_debug("Starting run")
                run_id = self.reporter.start_run()
                self.logger.log_debug(f"Run ID: {run_id}")
                self.overhead += time.time() - ts
                return run_id
            except Exception as e:
                self.logger.log('Failed to start run, disabling reporting', 'info')
                self.logger.log(e, 'error')
                self.reporter = None

    def complete_run(self) -> None:
        if self.reporter:
            try:
                ts = time.time()
                self.logger.log_debug("Completing run")
                self.reporter.complete_run()
                self.logger.log_debug("Run completed")
                self.overhead += time.time() - ts
                self.logger.log(f"Overhead for Qase Report: {round(self.overhead * 1000)}ms", 'info')
            except Exception as e:
                # We don't want to disable reporting here
                self.logger.log('Failed to complete run', 'info')
                self.logger.log(e, 'error')

    def add_result(self, result: Result) -> None:
        if self.reporter:
            try:
                ts = time.time()
                self.logger.log_debug(f"Adding result {result}")
                self.reporter.add_result(result)
                self.logger.log_debug(f"Result {result.get_title()} added")
                self.overhead += time.time() - ts
            except Exception as e:
                # Log error, disable reporting and continue
                self.logger.log(f'Failed to add result {result.get_title()}', 'info')
                self.logger.log(e, 'error')
                self._run_fallback()

    def add_attachment(self, attachment: Attachment) -> None:
        if self.reporter:
            try:
                ts = time.time()
                self.logger.log_debug(f"Adding attachment {attachment}")
                self.reporter.add_attachment(attachment)
                self.logger.log_debug(f"Attachment {attachment.id} added")
                self.overhead += time.time() - ts
            except Exception as e:
                # Log error and run fallback
                self.logger.log('Failed to add attachment', 'info')
                self.logger.log(e, 'error')
                self._run_fallback()

    def setup_profilers(self, runtime: Runtime) -> None:
        profilers = self.config.profilers

        for profiler in profilers:
            if profiler == "network":
                # Lazy import
                from ..profilers import NetworkProfilerSingleton
                NetworkProfilerSingleton.init(runtime=runtime,
                                              skip_domain=self.config.testops.api.host)
                self.profilers.append(NetworkProfilerSingleton.get_instance())
            if profiler == "sleep":
                from ..profilers import SleepProfiler
                self.profilers.append(SleepProfiler(runtime=runtime))
            if profiler == "db":
                from ..profilers import DbProfiler
                self.profilers.append(DbProfiler(runtime=runtime))

    def enable_profilers(self) -> None:
        if self.reporter:
            for profiler in self.profilers:
                profiler.enable()

    def disable_profilers(self) -> None:
        if self.reporter:
            for profiler in self.profilers:
                profiler.disable()

    def set_run_id(self, run_id: str) -> None:
        if self.reporter:
            try:
                self.reporter.set_run_id(run_id)
            except Exception as e:
                # Log error and run fallback
                self.logger.log('Failed to set run id', 'info')
                self.logger.log(e, 'error')
                self._run_fallback()

    def complete_worker(self) -> None:
        if self.reporter:
            try:
                self.reporter.complete_worker()
            except Exception as e:
                # Log error and run fallback
                self.logger.log('Failed to complete worker', 'info')
                self.logger.log(e, 'error')
                self._run_fallback()

    def _run_fallback(self) -> None:
        if self.fallback:
            try:
                results = self.reporter.get_results()

                self.fallback.start_run()
                self.reporter = self.fallback
                self.reporter.set_results(results)
                self.fallback = None
            except Exception as e:
                # Log error, disable reporting and continue
                self.logger.log('Failed to run fallback', 'info')
                self.logger.log(e, 'error')
                self.reporter = None

    def _load_testops_plan(self) -> None:
        try:
            if self.config.testops.plan.id is not None:
                from .. import TestOpsPlanLoader

                # Load test plan data from Qase TestOps
                loader = TestOpsPlanLoader(
                    api_token=self.config.testops.api.token,
                    host=self.config.testops.api.host
                )
                self.execution_plan = loader.load(self.config.testops.project,
                                                  int(self.config.testops.plan.id))
        except Exception as e:
            self.logger.log('Failed to load test plan from Qase TestOps', 'info')
            self.logger.log(e, 'error')

    # TODO: won't work, need to fix
    # def _selective_execution_setup(self) -> list:
    #     # Load execution plan from file
    #     path = self.config.execution_plan.path
    #     if not self.config.execution_plan.path and path and os.path.isfile(self.config.execution_plan.path):
    #         with open(self.config.execution_plan.path) as f:
    #             return json.load(f)
    #
    #     # Load execution plan from command line or env variable
    #     if self.config.self.config.execution_plan.path:
    #         return [int(n) for n in str(self.config.self.config.execution_plan.path.split(","))]

    def _fallback_setup(self) -> Union[QaseReport, None]:
        if self.config.fallback == Mode.report:
            return QaseReport(config=self.config, logger=self.logger)
        return None
