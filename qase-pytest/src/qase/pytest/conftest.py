from .plugin import QasePytestPlugin, QasePytestPluginSingleton

from qase.commons.reporters import QaseCoreReporter

from .options import QasePytestOptions
from qase.commons.config import ConfigManager


def pytest_addoption(parser):
    group = parser.getgroup("qase")
    QasePytestOptions.addoptions(parser, group)


def pytest_configure(config):
    config = _add_markers(config)
    config.addinivalue_line(
        "markers",
        "qase_parametrize_ignore: mark test to ignore parameters in Qase reports"
    )

    config_manager = setup_config_manager(config)

    QasePytestPluginSingleton.init(reporter=QaseCoreReporter(
        config_manager, 'pytest', 'qase-pytest'))
    config.qase = QasePytestPluginSingleton.get_instance()
    config.pluginmanager.register(
        config.qase,
        name="qase-pytest",
    )


def _add_markers(config):
    config.addinivalue_line(
        "markers", "qase_id: mark test to be associate with Qase TestOps test case")
    config.addinivalue_line("markers", "qase_title: mark test with title")
    config.addinivalue_line(
        "markers", "qase_ignore: skip test from Qase TestOps and Qase Report")
    config.addinivalue_line(
        "markers", "qase_muted: mark test as muted so it will not affect test run status")
    config.addinivalue_line("markers", "qase_author: mark test with author")
    config.addinivalue_line("markers", "qase_fields: mark test with meta data")
    config.addinivalue_line("markers", "qase_suite: mark test with suite")

    # Legacy markers | These markers are deprecated and will be removed in future versions
    config.addinivalue_line(
        "markers", "qase_description: mark test with description")
    config.addinivalue_line(
        "markers", "qase_preconditions: mark test with preconditions")
    config.addinivalue_line(
        "markers", "qase_postconditions: mark test with postconditions")
    config.addinivalue_line("markers", "qase_layer: mark test with layer")
    config.addinivalue_line(
        "markers", "qase_severity: mark test with severity")
    config.addinivalue_line(
        "markers", "qase_priority: mark test with priority")
    config.addinivalue_line("markers", "qase_tags: mark test with tags")
    return config


def setup_config_manager(config):
    config_manager = ConfigManager()
    for option in config.option.__dict__:
        if option == "output" and config.option.__dict__[option] is not None:
            config_manager.config.framework.playwright.set_output_dir(
                config.option.__dict__[option])

        if option == "video" and config.option.__dict__[option] is not None:
            config_manager.config.framework.playwright.set_video(
                config.option.__dict__[option])

        if option == "tracing" and config.option.__dict__[option] is not None:
            config_manager.config.framework.playwright.set_trace(
                config.option.__dict__[option])

        if option.startswith("qase_"):
            if option == "qase_mode" and config.option.__dict__[option] is not None:
                config_manager.config.set_mode(config.option.__dict__[option])

            if option == "qase_fallback" and config.option.__dict__[option] is not None:
                config_manager.config.set_fallback(
                    config.option.__dict__[option])

            if option == "qase_environment" and config.option.__dict__[option] is not None:
                config_manager.config.set_environment(
                    config.option.__dict__[option])

            if option == "qase_profilers" and config.option.__dict__[option] is not None:
                config_manager.config.set_profilers(
                    config.option.__dict__[option].split(","))

            if option == "qase_root_suite" and config.option.__dict__[option] is not None:
                config_manager.config.set_root_suite(
                    config.option.__dict__[option])

            if option == "qase_debug" and config.option.__dict__[option] is not None:
                config_manager.config.set_debug(config.option.__dict__[option])

            if option == "qase_exclude_params" and config.option.__dict__[option] is not None:
                config_manager.config.set_exclude_params(
                    [param.strip() for param in config.option.__dict__[option].split(',')])

            if option == "qase_execution_plan_path" and config.option.__dict__[option] is not None:
                config_manager.config.execution_plan.set_path(
                    config.option.__dict__[option])

            if option == "qase_testops_project" and config.option.__dict__[option] is not None:
                config_manager.config.testops.set_project(
                    config.option.__dict__[option])

            if option == "qase_testops_api_token" and config.option.__dict__[option] is not None:
                config_manager.config.testops.api.set_token(
                    config.option.__dict__[option])

            if option == "qase_testops_api_host" and config.option.__dict__[option] is not None:
                config_manager.config.testops.api.set_host(
                    config.option.__dict__[option])

            if option == "qase_testops_plan_id" and config.option.__dict__[option] is not None:
                config_manager.config.testops.plan.set_id(
                    int(config.option.__dict__[option]))

            if option == "qase_testops_run_id" and config.option.__dict__[option] is not None:
                config_manager.config.testops.run.set_id(
                    int(config.option.__dict__[option]))

            if option == "qase_testops_run_title" and config.option.__dict__[option] is not None:
                config_manager.config.testops.run.set_title(
                    config.option.__dict__[option])

            if option == "qase_testops_run_description" and config.option.__dict__[option] is not None:
                config_manager.config.testops.run.set_description(
                    config.option.__dict__[option])

            if option == "qase_testops_run_complete" and config.option.__dict__[option] is not None:
                config_manager.config.testops.run.set_complete(
                    config.option.__dict__[option])

            if option == "qase_testops_run_tags" and config.option.__dict__[option] is not None:
                config_manager.config.testops.run.set_tags(
                    [tag.strip() for tag in config.option.__dict__[option].split(',')])

            if option == "qase_testops_defect" and config.option.__dict__[option] is not None:
                config_manager.config.testops.set_defect(
                    config.option.__dict__[option])

            if option == "qase_report_driver" and config.option.__dict__[option] is not None:
                config_manager.config.report.set_driver(
                    config.option.__dict__[option])

            if option == "qase_report_connection_local_path" and config.option.__dict__[option] is not None:
                config_manager.config.report.connection.set_path(
                    config.option.__dict__[option])

            if option == "qase_report_connection_local_format" and config.option.__dict__[option] is not None:
                config_manager.config.report.connection.set_format(
                    config.option.__dict__[option])

            if option == "qase_testops_batch_size" and config.option.__dict__[option] is not None:
                config_manager.config.testops.batch.set_size(
                    int(config.option.__dict__[option]))

            if option == "qase_pytest_capture_logs" and config.option.__dict__[option] is not None:
                config_manager.config.framework.pytest.set_capture_logs(
                    config.option.__dict__[option])

            if option == "qase_pytest_xfail_status" and config.option.__dict__[option] is not None:
                config_manager.config.framework.pytest.xfail_status.set_xfail(
                    config.option.__dict__[option])

            if option == "qase_pytest_xpass_status" and config.option.__dict__[option] is not None:
                config_manager.config.framework.pytest.xfail_status.set_xpass(
                    config.option.__dict__[option])

            if option == "qase_testops_configurations_values" and config.option.__dict__[option] is not None:
                # Parse configurations from CLI parameter
                # Format: "group1=value1,group2=value2"
                config_pairs = config.option.__dict__[option].split(',')
                for pair in config_pairs:
                    if '=' in pair:
                        name, config_value = pair.split('=', 1)
                        config_manager.config.testops.configurations.add_value(name.strip(), config_value.strip())

            if option == "qase_testops_configurations_create_if_not_exists" and config.option.__dict__[option] is not None:
                config_manager.config.testops.configurations.set_create_if_not_exists(
                    config.option.__dict__[option])

    return config_manager


def pytest_unconfigure(config):
    qase = getattr(config, "src", None)
    if qase:
        del config.qase
        config.pluginmanager.unregister(qase)
