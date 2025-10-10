from qase.commons import ConfigManager
from qase.commons.reporters import QaseCoreReporter

from .plugin import QasePytestPluginSingleton
from .options import QasePytestOptions


def pytest_addoption(parser):
    group = parser.getgroup("qase")
    QasePytestOptions.addoptions(parser, group)

def _add_markers(config):
    config.addinivalue_line("markers", "qase_id: mark test to be associate with Qase TestOps test case")
    config.addinivalue_line("markers", "qase_title: mark test with title")
    config.addinivalue_line("markers", "qase_ignore: skip test from Qase TestOps and Qase Report")
    config.addinivalue_line("markers", "qase_muted: mark test as muted so it will not affect test run status")
    config.addinivalue_line("markers", "qase_author: mark test with author")
    config.addinivalue_line("markers", "qase_fields: mark test with meta data")
    config.addinivalue_line("markers", "qase_suite: mark test with suite")

    # Legacy markers | These markers are deprecated and will be removed in future versions
    config.addinivalue_line("markers", "qase_description: mark test with description")
    config.addinivalue_line("markers", "qase_preconditions: mark test with preconditions")
    config.addinivalue_line("markers", "qase_postconditions: mark test with postconditions")
    config.addinivalue_line("markers", "qase_layer: mark test with layer")
    config.addinivalue_line("markers", "qase_severity: mark test with severity")
    config.addinivalue_line("markers", "qase_priority: mark test with priority")
    config.addinivalue_line("markers", "qase_tags: mark test with tags")
    return config


def pytest_configure(config):
    config = _add_markers(config)

    config_manager = setup_config_manager(config)

    QasePytestPluginSingleton.init(reporter=QaseCoreReporter(config_manager, 'tavern', 'qase-tavern'))
    config.qase = QasePytestPluginSingleton.get_instance()
    config.pluginmanager.register(
        config.qase,
        name="qase-tavern",
    )


def pytest_unconfigure(config):
    qase = getattr(config, "src", None)
    if qase:
        del config.qase
        config.pluginmanager.unregister(qase)


def setup_config_manager(config):
    config_manager = ConfigManager()
    for option in config.option.__dict__:
        if option == "output" and config.option.__dict__[option] is not None:
            config_manager.config.framework.playwright.set_output_dir(config.option.__dict__[option])

        if option == "video" and config.option.__dict__[option] is not None:
            config_manager.config.framework.playwright.set_video(config.option.__dict__[option])

        if option == "tracing" and config.option.__dict__[option] is not None:
            config_manager.config.framework.playwright.set_trace(config.option.__dict__[option])

        if option.startswith("qase_"):
            if option == "qase_mode" and config.option.__dict__[option] is not None:
                config_manager.config.set_mode(config.option.__dict__[option])

            if option == "qase_fallback" and config.option.__dict__[option] is not None:
                config_manager.config.set_fallback(config.option.__dict__[option])

            if option == "qase_environment" and config.option.__dict__[option] is not None:
                config_manager.config.set_environment(config.option.__dict__[option])

            if option == "qase_profilers" and config.option.__dict__[option] is not None:
                config_manager.config.set_profilers(config.option.__dict__[option].split(","))

            if option == "qase_root_suite" and config.option.__dict__[option] is not None:
                config_manager.config.set_root_suite(config.option.__dict__[option])

            if option == "qase_debug" and config.option.__dict__[option] is not None:
                config_manager.config.set_debug(config.option.__dict__[option])

            if option == "qase_exclude_params" and config.option.__dict__[option] is not None:
                config_manager.config.set_exclude_params(
                    [param.strip() for param in config.option.__dict__[option].split(',')])

            if option == "qase_execution_plan_path" and config.option.__dict__[option] is not None:
                config_manager.config.execution_plan.set_path(config.option.__dict__[option])

            if option == "qase_testops_project" and config.option.__dict__[option] is not None:
                config_manager.config.testops.set_project(config.option.__dict__[option])

            if option == "qase_testops_api_token" and config.option.__dict__[option] is not None:
                config_manager.config.testops.api.set_token(config.option.__dict__[option])

            if option == "qase_testops_api_host" and config.option.__dict__[option] is not None:
                config_manager.config.testops.api.set_host(config.option.__dict__[option])

            if option == "qase_testops_plan_id" and config.option.__dict__[option] is not None:
                config_manager.config.testops.plan.set_id(int(config.option.__dict__[option]))

            if option == "qase_testops_run_id" and config.option.__dict__[option] is not None:
                config_manager.config.testops.run.set_id(int(config.option.__dict__[option]))

            if option == "qase_testops_run_title" and config.option.__dict__[option] is not None:
                config_manager.config.testops.run.set_title(config.option.__dict__[option])

            if option == "qase_testops_run_description" and config.option.__dict__[option] is not None:
                config_manager.config.testops.run.set_description(config.option.__dict__[option])

            if option == "qase_testops_run_complete" and config.option.__dict__[option] is not None:
                config_manager.config.testops.run.set_complete(config.option.__dict__[option])

            if option == "qase_testops_run_tags" and config.option.__dict__[option] is not None:
                config_manager.config.testops.run.set_tags(
                    [tag.strip() for tag in config.option.__dict__[option].split(',')])

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

            if option == "qase_testops_status_filter" and config.option.__dict__[option] is not None:
                config_manager.config.testops.set_status_filter(
                    [status.strip() for status in config.option.__dict__[option].split(',')])

            if option == "qase_testops_show_public_report_link" and config.option.__dict__[option] is not None:
                config_manager.config.testops.set_show_public_report_link(
                    config.option.__dict__[option])

            if option == "qase_status_mapping" and config.option.__dict__[option] is not None:
                # Parse status mapping from CLI parameter
                # Format: "source1=target1,source2=target2"
                mapping_dict = {}
                pairs = config.option.__dict__[option].split(',')
                for pair in pairs:
                    pair = pair.strip()
                    if pair and '=' in pair:
                        source_status, target_status = pair.split('=', 1)
                        mapping_dict[source_status.strip()] = target_status.strip()
                config_manager.config.set_status_mapping(mapping_dict)

            if option == "qase_testops_run_external_link_type" and config.option.__dict__[option] is not None:
                if not config_manager.config.testops.run.external_link:
                    from qase.commons.models.external_link import ExternalLinkConfig
                    config_manager.config.testops.run.external_link = ExternalLinkConfig()
                config_manager.config.testops.run.external_link.set_type(config.option.__dict__[option])

            if option == "qase_testops_run_external_link_url" and config.option.__dict__[option] is not None:
                if not config_manager.config.testops.run.external_link:
                    from qase.commons.models.external_link import ExternalLinkConfig
                    config_manager.config.testops.run.external_link = ExternalLinkConfig()
                config_manager.config.testops.run.external_link.set_link(config.option.__dict__[option])

            if option == "qase_testops_defect" and config.option.__dict__[option] is not None:
                config_manager.config.testops.set_defect(config.option.__dict__[option])

            if option == "qase_report_driver" and config.option.__dict__[option] is not None:
                config_manager.config.report.set_driver(config.option.__dict__[option])

            if option == "qase_report_connection_local_path" and config.option.__dict__[option] is not None:
                config_manager.config.report.connection.set_path(config.option.__dict__[option])

            if option == "qase_report_connection_local_format" and config.option.__dict__[option] is not None:
                config_manager.config.report.connection.set_format(config.option.__dict__[option])

            if option == "qase_testops_batch_size" and config.option.__dict__[option] is not None:
                config_manager.config.testops.batch.set_size(int(config.option.__dict__[option]))

            if option == "qase_pytest_capture_logs" and config.option.__dict__[option] is not None:
                config_manager.config.framework.pytest.set_capture_logs(config.option.__dict__[option])

            if option == "qase_logging_console" and config.option.__dict__[option] is not None:
                config_manager.config.logging.set_console(config.option.__dict__[option])

            if option == "qase_logging_file" and config.option.__dict__[option] is not None:
                config_manager.config.logging.set_file(config.option.__dict__[option])

    # Update logger with final logging options after all CLI options are processed
    from qase.commons.logger import LoggingOptions
    logging_options = LoggingOptions(
        console=config_manager.config.logging.console if config_manager.config.logging.console is not None else True,
        file=config_manager.config.logging.file if config_manager.config.logging.file is not None else config_manager.config.debug
    )
    config_manager.logger = config_manager.logger.__class__(debug=config_manager.config.debug, logging_options=logging_options)

    return config_manager
