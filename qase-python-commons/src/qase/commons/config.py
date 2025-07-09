import os
import json
from .logger import Logger
from .models.config.qaseconfig import QaseConfig, Mode


class ConfigManager:

    def __init__(self, config_file='./qase.config.json'):
        self.logger = Logger()
        self.__config_file = config_file
        self.config = QaseConfig()

        self.__load_file_config()
        self.__load_env_config()

    def validate_config(self):
        errors: list[str] = []
        if self.config.mode is Mode.testops or self.config.fallback is Mode.testops:
            if self.config.testops.api.token is None:
                errors.append("Testops token is not set")

            if self.config.testops.project is None:
                errors.append("Testops project is not set")

        if len(errors) > 0:
            self.logger.log("Config validation failed", "error")
            for error in errors:
                self.logger.log(error, "error")
            raise Exception("Config validation failed")

    def __str__(self):
        return json.dumps(self.config, indent=4, sort_keys=True)

    def __load_file_config(self):
        try:
            if os.path.exists(self.__config_file):
                with open(self.__config_file, "r") as file:
                    config = json.load(file)

                    if config.get("mode"):
                        self.config.set_mode(config.get("mode"))

                    if config.get("fallback"):
                        self.config.set_fallback(config.get("fallback"))

                    if config.get("environment"):
                        self.config.set_environment(config.get("environment"))

                    if config.get("rootSuite"):
                        self.config.set_root_suite(config.get("rootSuite"))

                    if config.get("profilers"):
                        self.config.set_profilers(config.get("profilers"))

                    if config.get("debug") is not None:
                        self.config.set_debug(
                            config.get("debug")
                        )

                    if config.get("excludeParams"):
                        self.config.set_exclude_params(
                            config.get("excludeParams")
                        )

                    if config.get("executionPlan"):
                        execution_plan = config.get("executionPlan")
                        if execution_plan.get("path"):
                            self.config.execution_plan.set_path(
                                execution_plan.get("path"))

                    if config.get("testops"):
                        testops = config.get("testops")

                        if testops.get("api"):
                            api = testops.get("api")

                            if api.get("host"):
                                self.config.testops.api.set_host(
                                    api.get("host"))

                            if api.get("token"):
                                self.config.testops.api.set_token(
                                    api.get("token"))

                        if testops.get("project"):
                            self.config.testops.set_project(
                                testops.get("project"))

                        if testops.get("defect") is not None:
                            self.config.testops.set_defect(
                                testops.get("defect")
                            )

                        if testops.get("plan"):
                            plan = testops.get("plan")

                            if plan.get("id"):
                                self.config.testops.plan.set_id(plan.get("id"))

                        if testops.get("run"):
                            run = testops.get("run")

                            if run.get("id"):
                                self.config.testops.run.set_id(run.get("id"))

                            if run.get("title"):
                                self.config.testops.run.set_title(
                                    run.get("title"))

                            if run.get("description"):
                                self.config.testops.run.set_description(
                                    run.get("description"))

                            if run.get("complete") is not None:
                                self.config.testops.run.set_complete(
                                    run.get("complete")
                                )

                            if run.get("tags"):
                                self.config.testops.run.set_tags(
                                    [tag.strip() for tag in run.get("tags")])

                        if testops.get("batch"):
                            batch = testops.get("batch")

                            if batch.get("size"):
                                self.config.testops.batch.set_size(
                                    batch.get("size"))

                        if testops.get("configurations"):
                            configurations = testops.get("configurations")

                            if configurations.get("values"):
                                values = configurations.get("values")
                                for value in values:
                                    if value.get("name") and value.get("value"):
                                        self.config.testops.configurations.add_value(
                                            value.get("name"), value.get("value"))

                            if configurations.get("createIfNotExists") is not None:
                                self.config.testops.configurations.set_create_if_not_exists(
                                    configurations.get("createIfNotExists"))

                    if config.get("report"):
                        report = config.get("report")

                        if report.get("driver"):
                            self.config.report.set_driver(report.get("driver"))

                        if report.get("connection"):
                            connection = report.get("connection")

                            if connection.get("path"):
                                self.config.report.connection.set_path(
                                    connection.get("path"))

                            if connection.get("format"):
                                self.config.report.connection.set_format(
                                    connection.get("format")
                                )

                    if config.get("framework"):
                        framework = config.get("framework")

                        if framework.get("pytest"):
                            pytest = framework.get("pytest")

                            if pytest.get("captureLogs") is not None:
                                self.config.framework.pytest.set_capture_logs(
                                    pytest.get("captureLogs")
                                )

                            if pytest.get("xfailStatus"):
                                xfail_status = pytest.get("xfailStatus")

                                if xfail_status.get("xfail"):
                                    self.config.framework.pytest.xfail_status.set_xfail(
                                        xfail_status.get("xfail")
                                    )

                                if xfail_status.get("xpass"):
                                    self.config.framework.pytest.xfail_status.set_xpass(
                                        xfail_status.get("xpass")
                                    )

        except Exception as e:
            self.logger.log("Failed to load config from file", "error")

    def __load_env_config(self):
        try:
            for key, value in os.environ.items():
                if key == 'QASE_MODE':
                    self.config.set_mode(value)

                if key == 'QASE_FALLBACK':
                    self.config.set_fallback(value)

                if key == 'QASE_ENVIRONMENT':
                    self.config.set_environment(value)

                if key == 'QASE_ROOT_SUITE':
                    self.config.set_root_suite(value)

                if key == 'QASE_PROFILERS':
                    self.config.set_profilers(value.split(','))

                if key == 'QASE_DEBUG':
                    self.config.set_debug(value)

                if key == 'QASE_EXCLUDE_PARAMS':
                    self.config.set_exclude_params(
                        [param.strip() for param in value.split(',')])

                if key == 'QASE_EXECUTION_PLAN_PATH':
                    self.config.execution_plan.set_path(value)

                if key == 'QASE_TESTOPS_API_HOST':
                    self.config.testops.api.set_host(value)

                if key == 'QASE_TESTOPS_API_TOKEN':
                    self.config.testops.api.set_token(value)

                if key == 'QASE_TESTOPS_PROJECT':
                    self.config.testops.set_project(value)

                if key == 'QASE_TESTOPS_DEFECT':
                    self.config.testops.set_defect(value)

                if key == 'QASE_TESTOPS_PLAN_ID':
                    self.config.testops.plan.set_id(value)

                if key == 'QASE_TESTOPS_RUN_ID':
                    self.config.testops.run.set_id(value)

                if key == 'QASE_TESTOPS_RUN_TITLE':
                    self.config.testops.run.set_title(value)

                if key == 'QASE_TESTOPS_RUN_DESCRIPTION':
                    self.config.testops.run.set_description(value)

                if key == 'QASE_TESTOPS_RUN_COMPLETE':
                    self.config.testops.run.set_complete(value)

                if key == 'QASE_TESTOPS_RUN_TAGS':
                    self.config.testops.run.set_tags(
                        [tag.strip() for tag in value.split(',')])

                if key == 'QASE_TESTOPS_BATCH_SIZE':
                    self.config.testops.batch.set_size(value)

                if key == 'QASE_TESTOPS_CONFIGURATIONS_VALUES':
                    # Parse configurations from environment variable
                    # Format: "group1=value1,group2=value2"
                    if value:
                        config_pairs = value.split(',')
                        for pair in config_pairs:
                            if '=' in pair:
                                name, config_value = pair.split('=', 1)
                                self.config.testops.configurations.add_value(name.strip(), config_value.strip())

                if key == 'QASE_TESTOPS_CONFIGURATIONS_CREATE_IF_NOT_EXISTS':
                    self.config.testops.configurations.set_create_if_not_exists(value)

                if key == 'QASE_REPORT_DRIVER':
                    self.config.report.set_driver(value)

                if key == 'QASE_REPORT_CONNECTION_PATH':
                    self.config.report.connection.set_path(value)

                if key == 'QASE_REPORT_CONNECTION_FORMAT':
                    self.config.report.connection.set_format(value)

                if key == 'QASE_PYTEST_CAPTURE_LOGS':
                    self.config.framework.pytest.set_capture_logs(value)

                if key == 'QASE_PYTEST_XFAIL_STATUS_XFAIL':
                    self.config.framework.pytest.xfail_status.set_xfail(value)

                if key == 'QASE_PYTEST_XFAIL_STATUS_XPASS':
                    self.config.framework.pytest.xfail_status.set_xpass(value)

        except Exception as e:
            self.logger.log("Failed to load config from env vars {e}", "error")
