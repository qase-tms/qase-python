import os

from behave.formatter.base import Formatter
from behave.model import Feature, Scenario, Step
from qase.commons import ConfigManager
from qase.commons.reporters import QaseCoreReporter

from qase.behave.utils import (
    filter_scenarios, parse_scenario, parse_step,
    parse_scenario_from_json, parse_step_from_json,
)
from qase.behave.qase_global import qase


class QaseFormatter(Formatter):
    name = 'qase'
    description = 'Qase.io formatter'

    # Lock file paths for BehaveX worker coordination
    _run_id_file = "qase_behavex_run_id"
    _lock_file = "qase_behavex.lock"

    def __init__(self, stream_opener=None, config=None):
        self._behavex_mode = stream_opener is None and config is None
        self._is_behavex_worker = False
        self.__already_started = False
        self.__case_ids = []
        self.__current_scenario = None

        if not self._behavex_mode:
            super().__init__(stream_opener, config)
            userdata = config.userdata
            self._is_behavex_worker = 'worker_id' in userdata

            cfg = self.__parse_config(userdata)
            self.reporter = QaseCoreReporter(cfg, 'behave', 'qase-behave')

            if self._is_behavex_worker:
                self._init_worker_run()
        else:
            self.reporter = None

    def _init_worker_run(self):
        """Initialize run in BehaveX worker mode with lock file coordination."""
        from filelock import FileLock

        with FileLock(self._lock_file):
            if os.path.exists(self._run_id_file):
                with open(self._run_id_file, "r") as f:
                    run_id = f.read().strip()
                self.reporter.set_run_id(run_id)
            else:
                run_id = self.reporter.start_run()
                with open(self._run_id_file, "w") as f:
                    f.write(str(run_id))

        self.__already_started = True

    def uri(self, uri):
        if self.__already_started:
            return

        if not self._is_behavex_worker:
            self.reporter.start_run()

        execution_plan = self.reporter.get_execution_plan()
        self.__case_ids = execution_plan if execution_plan else []
        self.__already_started = True

    def feature(self, feature: Feature):
        feature.scenarios = filter_scenarios(
            self.__case_ids, feature.scenarios)

    def scenario(self, scenario: Scenario):
        if self.__current_scenario and self.__current_scenario.ignore == False:
            self.__current_scenario.execution.complete()
            self.reporter.add_result(self.__current_scenario)
            self.__current_scenario = None
        self.__current_scenario = parse_scenario(scenario)
        qase._set_current_scenario(self.__current_scenario)
        qase._set_current_step(None)

    def result(self, result: Step):
        step = parse_step(result)
        qase._set_current_step(step)

        if step.execution.status != 'passed':
            is_assertion_error = False
            if result.error_message:
                assertion_keywords = ['assert', 'AssertionError', 'expect', 'should', 'must']
                is_assertion_error = any(keyword in result.error_message for keyword in assertion_keywords)

            if step.execution.status == 'failed':
                status = 'failed' if is_assertion_error else 'invalid'
                step.execution.set_status(status)
                self.__current_scenario.execution.set_status(status)
            else:
                self.__current_scenario.execution.set_status(step.execution.status)

            if result.error_message:
                self.__current_scenario.execution.stacktrace = result.error_message
        self.__current_scenario.steps.append(step)
        qase._set_current_step(None)

    def eof(self):
        if self.__current_scenario and self.__current_scenario.ignore == False:
            self.__current_scenario.execution.complete()
            self.reporter.add_result(self.__current_scenario)
            self.__current_scenario = None

    def close(self):
        if self._is_behavex_worker:
            self.reporter.complete_worker()
        else:
            self.reporter.complete_worker()
            self.reporter.complete_run()

    def launch_json_formatter(self, json_data):
        """BehaveX post-execution formatter entry point.

        Called by BehaveX's FormatterManager after all parallel workers complete.
        Receives consolidated JSON with all test results.
        """
        if self.reporter is None:
            cfg = ConfigManager()
            self.reporter = QaseCoreReporter(cfg, 'behave', 'qase-behave')

        # Check if workers already sent results (lock file exists)
        if os.path.exists(self._run_id_file):
            with open(self._run_id_file, "r") as f:
                run_id = f.read().strip()
            self.reporter.set_run_id(run_id)
            self.reporter.complete_run()
            self._cleanup_lock_files()
            return

        # Workers didn't run QaseFormatter — process JSON ourselves
        self.reporter.start_run()

        for feature in json_data.get('features', []):
            feature_filename = feature.get('filename', '')
            for scenario_dict in feature.get('scenarios', []):
                result = parse_scenario_from_json(scenario_dict, feature_filename)

                if result.ignore:
                    continue

                # Background steps first
                background = scenario_dict.get('background', {})
                for step_dict in background.get('steps', []):
                    step = parse_step_from_json(step_dict)
                    result.steps.append(step)

                # Regular steps
                for step_dict in scenario_dict.get('steps', []):
                    step = parse_step_from_json(step_dict)
                    result.steps.append(step)

                self.reporter.add_result(result)

        self.reporter.complete_worker()
        self.reporter.complete_run()

    def _cleanup_lock_files(self):
        """Remove lock and run_id files."""
        for path in (self._run_id_file, self._lock_file):
            try:
                os.remove(path)
            except FileNotFoundError:
                pass

    @staticmethod
    def __parse_config(userdata) -> ConfigManager:
        cfg_mgr = ConfigManager()

        if 'qase-mode' in userdata:
            cfg_mgr.config.set_mode(userdata['qase-mode'])

        if 'qase-fallback' in userdata:
            cfg_mgr.config.set_fallback(userdata['qase-fallback'])

        if 'qase-environment' in userdata:
            cfg_mgr.config.set_environment(userdata['qase-environment'])

        if 'qase-root-suite' in userdata:
            cfg_mgr.config.set_root_suite(userdata['qase-root-suite'])

        if 'qase-debug' in userdata:
            cfg_mgr.config.set_debug(userdata['qase-debug'])

        if 'qase-exclude-params' in userdata:
            cfg_mgr.config.set_exclude_params(
                [param.strip() for param in userdata['qase-exclude-params'].split(',')])

        if 'qase-testops-project' in userdata:
            cfg_mgr.config.testops.set_project(
                userdata['qase-testops-project'])

        if 'qase-testops-api-token' in userdata:
            cfg_mgr.config.testops.api.set_token(
                userdata['qase-testops-api-token'])

        if 'qase-testops-api-host' in userdata:
            cfg_mgr.config.testops.api.set_host(
                userdata['qase-testops-api-host'])

        if 'qase-testops-run-title' in userdata:
            cfg_mgr.config.testops.run.set_title(
                userdata['qase-testops-run-title'])

        if 'qase-testops-run-description' in userdata:
            cfg_mgr.config.testops.run.set_description(
                userdata['qase-testops-run-description'])

        if 'qase-testops-run-complete' in userdata:
            cfg_mgr.config.testops.run.set_complete(
                userdata['qase-testops-run-complete'])

        if 'qase-testops-run-tags' in userdata:
            cfg_mgr.config.testops.run.set_tags(
                [tag.strip() for tag in userdata['qase-testops-run-tags'].split(',')])

        if 'qase-testops-run-external-link-type' in userdata:
            if not cfg_mgr.config.testops.run.external_link:
                from qase.commons.models.external_link import ExternalLinkConfig
                cfg_mgr.config.testops.run.external_link = ExternalLinkConfig()
            cfg_mgr.config.testops.run.external_link.set_type(userdata['qase-testops-run-external-link-type'])

        if 'qase-testops-run-external-link-url' in userdata:
            if not cfg_mgr.config.testops.run.external_link:
                from qase.commons.models.external_link import ExternalLinkConfig
                cfg_mgr.config.testops.run.external_link = ExternalLinkConfig()
            cfg_mgr.config.testops.run.external_link.set_link(userdata['qase-testops-run-external-link-url'])

        if 'qase-testops-plan-id' in userdata:
            cfg_mgr.config.testops.plan.set_id(
                userdata['qase-testops-plan-id'])

        if 'qase-testops-run-id' in userdata:
            cfg_mgr.config.testops.run.set_id(userdata['qase-testops-run-id'])

        if 'qase-execution-plan-path' in userdata:
            cfg_mgr.config.execution_plan.set_path(
                userdata['qase-execution-plan-path'])

        if 'qase-testops-batch-size' in userdata:
            cfg_mgr.config.testops.batch.set_size(
                userdata['qase-testops-batch-size'])

        if 'qase-testops-defect' in userdata:
            cfg_mgr.config.testops.set_defect(userdata['qase-testops-defect'])

        if 'qase-testops-configurations-values' in userdata:
            # Parse configurations from userdata
            # Format: "group1=value1,group2=value2"
            config_pairs = userdata['qase-testops-configurations-values'].split(',')
            for pair in config_pairs:
                if '=' in pair:
                    name, config_value = pair.split('=', 1)
                    cfg_mgr.config.testops.configurations.add_value(name.strip(), config_value.strip())

        if 'qase-testops-configurations-create-if-not-exists' in userdata:
            cfg_mgr.config.testops.configurations.set_create_if_not_exists(
                userdata['qase-testops-configurations-create-if-not-exists'])

        if 'qase-testops-status-filter' in userdata:
            cfg_mgr.config.testops.set_status_filter(
                [status.strip() for status in userdata['qase-testops-status-filter'].split(',')])

        if 'qase-testops-show-public-report-link' in userdata:
            cfg_mgr.config.testops.set_show_public_report_link(
                userdata['qase-testops-show-public-report-link'])

        if 'qase-status-mapping' in userdata:
            # Parse status mapping from userdata
            # Format: "source1=target1,source2=target2"
            mapping_dict = {}
            pairs = userdata['qase-status-mapping'].split(',')
            for pair in pairs:
                pair = pair.strip()
                if pair and '=' in pair:
                    source_status, target_status = pair.split('=', 1)
                    mapping_dict[source_status.strip()] = target_status.strip()
            cfg_mgr.config.set_status_mapping(mapping_dict)

        if 'qase-report-driver' in userdata:
            cfg_mgr.config.report.set_driver(userdata['qase-report-driver'])

        if 'qase-report-connection-path' in userdata:
            cfg_mgr.config.report.connection.set_path(
                userdata['qase-report-connection-path'])

        if 'qase-report-connection-format' in userdata:
            cfg_mgr.config.report.connection.set_format(
                userdata['qase-report-connection-format'])

        if 'qase-logging-console' in userdata:
            cfg_mgr.config.logging.set_console(userdata['qase-logging-console'])

        if 'qase-logging-file' in userdata:
            cfg_mgr.config.logging.set_file(userdata['qase-logging-file'])

        # Update logger with final logging options after all options are processed
        from qase.commons.logger import LoggingOptions
        logging_options = LoggingOptions(
            console=cfg_mgr.config.logging.console if cfg_mgr.config.logging.console is not None else True,
            file=cfg_mgr.config.logging.file if cfg_mgr.config.logging.file is not None else cfg_mgr.config.debug
        )
        cfg_mgr.logger = cfg_mgr.logger.__class__(debug=cfg_mgr.config.debug, logging_options=logging_options)

        return cfg_mgr
