import time

from ..config import ConfigManager
from ..logger import Logger

from .report import QaseReport
from .testops import QaseTestOps
from .testops_multi import QaseTestOpsMulti

from ..models import Result, Attachment, Runtime
from ..models.config.qaseconfig import Mode
from typing import Union, List, Dict

from ..util import get_host_info
from ..status_mapping.status_mapping import StatusMapping

"""
    CoreReporter is a facade for all reporters and it is used to initialize and manage them.
    It is also used to pass configuration and logger to reporters, handle fallback logic and error handling.
"""


class QaseCoreReporter:
    def __init__(self, config: ConfigManager, framework: Union[str, None] = None,
                 reporter_name: Union[str, None] = None):
        config.validate_config()
        self.config = config.config
        # Use the logger from ConfigManager instead of creating a new one
        self.logger = config.logger
        self._execution_plan = None
        self.profilers = []
        self.overhead = 0

        # Initialize status mapping
        self.status_mapping = StatusMapping.from_dict(self.config.status_mapping)
        if not self.status_mapping.is_empty():
            self.logger.log_debug(f"Status mapping initialized: {self.status_mapping}")

        # self._selective_execution_setup()
        self.fallback = self._fallback_setup()

        self.logger.log_debug(f"Config: {self.config}")

        host_data = get_host_info(framework, reporter_name)
        self.logger.log_debug(f"Host data: {host_data}")

        # Store framework and reporter_name for passing to reporters
        self.framework = framework
        self.reporter_name = reporter_name
        self.host_data = host_data

        # Reading reporter mode from config file
        mode = self.config.mode

        if mode == Mode.testops:
            try:
                self._load_testops_plan()
                # Create API client with host_data for headers
                from ..client.api_v2_client import ApiV2Client
                api_client = ApiV2Client(self.config, self.logger, host_data=host_data, 
                                       framework=framework, reporter_name=reporter_name)
                self.reporter = QaseTestOps(config=self.config, logger=self.logger, client=api_client)
            except Exception as e:
                self.logger.log('Failed to initialize TestOps reporter. Using fallback.', 'info')
                self.logger.log(e, 'error')
                self.reporter = self.fallback
        elif mode == Mode.testops_multi:
            try:
                # Create API client with host_data for headers
                from ..client.api_v2_client import ApiV2Client
                api_client = ApiV2Client(self.config, self.logger, host_data=host_data, 
                                       framework=framework, reporter_name=reporter_name)
                self.reporter = QaseTestOpsMulti(config=self.config, logger=self.logger, client=api_client)
            except Exception as e:
                self.logger.log('Failed to initialize TestOps Multi reporter. Using fallback.', 'info')
                self.logger.log(e, 'error')
                self.reporter = self.fallback
        elif mode == Mode.report:
            self.reporter = QaseReport(config=self.config, logger=self.logger)
        else:
            self.reporter = None

    def start_run(self) -> Union[str, Dict[str, str], None]:
        if self.reporter:
            try:
                ts = time.time()
                self.logger.log_debug("Starting run")
                run_id = self.reporter.start_run()
                if isinstance(run_id, dict):
                    # Multi-project mode returns dict of project -> run_id
                    self.logger.log_debug(f"Run IDs: {run_id}")
                else:
                    # Single project mode returns single run_id
                    self.logger.log_debug(f"Run ID: {run_id}")
                self.overhead += time.time() - ts
                return run_id
            except Exception as e:
                self.logger.log('Failed to start run, disabling reporting', 'info')
                self.logger.log(e, 'error')
                self.reporter = None
                return None

        return None

    def complete_run(self) -> None:
        if self.reporter:
            try:
                ts = time.time()
                self.reporter.complete_run()
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

                # Apply status mapping before adding result
                self._apply_status_mapping(result)

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
                from ..profilers import DatabaseProfilerSingleton
                DatabaseProfilerSingleton.init(runtime=runtime)
                self.profilers.append(DatabaseProfilerSingleton.get_instance())

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

    def get_execution_plan(self) -> Union[None, List[int]]:
        return self._execution_plan

    def _run_fallback(self) -> None:
        if self.fallback:
            try:
                results = self.reporter.get_results()

                self.fallback.start_run()
                self.reporter = self.fallback
                # Handle both single project (list) and multi-project (dict) results
                if isinstance(results, dict):
                    # Multi-project mode: results is dict of project -> list of results
                    for project_code, project_results in results.items():
                        self.reporter.set_results({project_code: project_results})
                else:
                    # Single project mode: results is list
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
                self._execution_plan = loader.load(self.config.testops.project,
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

    def _apply_status_mapping(self, result: Result) -> None:
        """
        Apply status mapping to a test result.
        
        This method applies the configured status mapping to the result's execution status.
        The mapping is applied before the result is sent to the reporter.
        
        Args:
            result: Test result to apply status mapping to
        """
        if self.status_mapping.is_empty():
            return
        
        original_status = result.get_status()
        if not original_status:
            return
        
        mapped_status = self.status_mapping.apply_mapping(original_status)
        
        if mapped_status != original_status:
            result.execution.set_status(mapped_status)
            self.logger.log_debug(f"Status mapped for '{result.get_title()}': {original_status} -> {mapped_status}")
