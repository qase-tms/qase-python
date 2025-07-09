from behave.formatter.base import Formatter
from behave.model import Feature, Scenario, Step
from qase.commons import ConfigManager
from qase.commons.reporters import QaseCoreReporter

from qase.behave.utils import filter_scenarios, parse_scenario, parse_step
from qase.behave.qase_global import qase


class QaseFormatter(Formatter):
    name = 'qase'
    description = 'Qase.io formatter'
    __already_started = False
    __case_ids = []
    __current_scenario = None

    def __init__(self, stream_opener, config):
        super(QaseFormatter, self).__init__(stream_opener, config)

        cfg = self.__parse_config(config.userdata)
        self.reporter = QaseCoreReporter(cfg, 'behave', 'qase-behave')

    def uri(self, uri):
        if not self.__already_started:
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
        # Update global qase object with current scenario
        qase._set_current_scenario(self.__current_scenario)
        pass

    def result(self, result: Step):
        step = parse_step(result)
        if step.execution.status != 'passed':
            self.__current_scenario.execution.set_status(step.execution.status)
            if result.error_message:
                self.__current_scenario.execution.stacktrace = result.error_message
        self.__current_scenario.steps.append(step)
        pass

    def eof(self):
        if self.__current_scenario and self.__current_scenario.ignore == False:
            self.__current_scenario.execution.complete()
            self.reporter.add_result(self.__current_scenario)
            self.__current_scenario = None
        pass

    def close(self):
        self.reporter.complete_worker()
        self.reporter.complete_run()
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

        if 'qase-report-driver' in userdata:
            cfg_mgr.config.report.set_driver(userdata['qase-report-driver'])

        if 'qase-report-connection-path' in userdata:
            cfg_mgr.config.report.connection.set_path(
                userdata['qase-report-connection-path'])

        if 'qase-report-connection-format' in userdata:
            cfg_mgr.config.report.connection.set_format(
                userdata['qase-report-connection-format'])

        return cfg_mgr
