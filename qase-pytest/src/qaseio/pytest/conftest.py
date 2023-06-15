from qaseio.pytest.plugin import QasePytestPlugin, QasePytestPluginSingleton

from qaseio.commons import QaseTestOps, QaseReport, ConfigManager
from qaseio.pytest.options import QasePytestOptions

import os
import json

def pytest_addoption(parser):
    group = parser.getgroup("qase")

    config_manager = ConfigManager()
    config_manager.load_config()

    for key in config_manager._get_keys(config_manager.config):
        default_value = config_manager.get(key)
        key_arg = key.replace("_", "-")
        group.addoption(f"--qase-{key_arg}", action="store", default=default_value)

    QasePytestOptions.addoptions(parser, group)

def pytest_configure(config):
    if not hasattr(config, "workerinput"):
        QasePytestPlugin.drop_run_id()
    config.addinivalue_line("markers", "qase_id: mark test to be associate with Qase TestOp test case")
    config.addinivalue_line("markers", "qase_title: mark test with title")
    config.addinivalue_line("markers", "qase_ignore: skip test from Qase TestOps \ Report")
    config.addinivalue_line("markers", "qase_muted: mark test as muted so it will not affect test run status")
    config.addinivalue_line("markers", "qase_author: mark test with author")
    config.addinivalue_line("markers", "qase_fields: mark test with meta data")
    config.addinivalue_line("markers", "qase_suite: mark test with suite")

    # Legacy markers
    config.addinivalue_line("markers", "qase_description: mark test with description")
    config.addinivalue_line("markers", "qase_preconditions: mark test with preconditions")
    config.addinivalue_line("markers", "qase_postconditions: mark test with postconditions")
    config.addinivalue_line("markers", "qase_layer: mark test with layer")
    config.addinivalue_line("markers", "qase_severity: mark test with severity")
    config.addinivalue_line("markers", "qase_priority: mark test with priority")
    config.addinivalue_line("markers", "qase_tags: mark test with tags")

    mode = config.getoption("qase_mode", None)
    execution_plan = None

    # Load execution plan from file
    path = config.getoption("qase_execution_plan_path", "qase_execution_plan.json")
    if not config.getoption("qase_execution_plan_path", None) and path and os.path.isfile(path):
        with open('execution_plan.json') as f:
            execution_plan = json.load(f)

    # Load execution plan from command line or env variable
    if config.getoption("qase_execution_plan", None):
        execution_plan = [int(n) for n in str(config.getoption("qase_execution_plan").split(","))]

    if mode:
        defaultReporter = QaseReport(
                report_path=config.getoption("qase_report_connection_local_path", "./build/qase-report"),
                format=config.getoption("qase_report_connection_local_format", "json"),
                environment=config.getoption("qase_environment", "local"),
            )
        if (mode == 'testops'):
            if validate_testops_options(config):
                if (config.getoption("qase_testops_plan_id", None) is not None):
                    from qaseio.commons import TestOpsPlanLoader

                    # Load test plan data from Qase TestOps
                    loader = TestOpsPlanLoader(
                        api_token=config.getoption("qase_testops_api_token"),
                        host=config.getoption("qase_testops_api_host", "qase.io"),
                    )
                    execution_plan = loader.load(config.getoption("qase_testops_project"),
                                                 int(config.getoption("qase_testops_plan_id")))

                reporter = QaseTestOps(
                    api_token=config.getoption("qase_testops_api_token"),
                    project_code=config.getoption("qase_testops_project"),
                    run_id=config.getoption("qase_testops_run_id", None),
                    plan_id=config.getoption("qase_testops_plan_id", None),
                    complete_run=config.getoption("qase_testops_run_complete", False),
                    bulk=config.getoption("qase_testops_bulk", True),
                    run_title=config.getoption("qase_testops_run_title", None),
                    host=config.getoption("qase_testops_api_host", "qase.io"),
                    chunk_size=config.getoption("qase_testops_chunk", 200),
                    environment=config.getoption("qase_environment", None),
                    defect=config.getoption("qase_testops_defect", False),
                )
                fallback = defaultReporter
            else:
                print('⚠️  Switching to local report mode')
                reporter = defaultReporter
                fallback = None
        else:
            reporter = defaultReporter
            fallback = None

        QasePytestPluginSingleton.init(
            reporter=reporter,
            fallback=fallback,
            xdist_enabled=is_xdist_enabled(config),
            capture_logs=config.getoption("qase_framework_pytest_capture_logs", False),
            intercept_requests=config.getoption("qase_framework_pytest_capture_http", False),
            execution_plan=execution_plan,
        )
        config.qaseio = QasePytestPluginSingleton.get_instance()
        config.pluginmanager.register(
            config.qaseio,
            name="qase-pytest",
        ) 

def validate_testops_options(config) -> bool:
    if not config.getoption("qase_testops_api_token", None):
        print("[QASE] ⚠️  Qase TestOps API token is required")
        return False
    
    if not config.getoption("qase_testops_project", None):
        print("[QASE] ⚠️  Qase TestOps project code is required")
        return False

    return True

def is_xdist_enabled(config):
    if (config.pluginmanager.getplugin("xdist") is not None and os.getenv('PYTEST_XDIST_WORKER_COUNT') is not None):
        return True
    return False

def pytest_unconfigure(config):
    qaseio = getattr(config, "src", None)
    if qaseio:
        del config.qaseio
        config.pluginmanager.unregister(qaseio)
