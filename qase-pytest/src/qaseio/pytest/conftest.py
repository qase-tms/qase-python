from qaseio.pytest.plugin import QasePytestPlugin, QasePytestPluginSingleton

from qaseio.pytest.testops import TestOps


def get_option_ini(config, name):
    ret = config.getoption(name)  # 'default' arg won't work as expected
    if ret in (None, False):
        ret = config.getini(name)
    return ret


def pytest_addoption(parser):
    group = parser.getgroup("qase")

    def add_option_ini(option, dest, default=None, type=None, **kwargs):
        parser.addini(
            dest,
            default=default,
            type=type,
            help="default value for " + option,
        )
        group.addoption(option, dest=dest, **kwargs)

    add_option_ini(
        "--qase-mode",
        "qs_mode",
        default="off",
        type="string",
        help="Define Qase reporter mode: `off` or `testops`"
    )

    add_option_ini(
        "--qase-environment",
        "qs_environment",
        help="Define environment slug or ID from TestOps",
    )

    """TestOps options"""
    add_option_ini(
        "--qase-to-api-token",
        "qs_to_api_token",
        help="Api token for Qase TestOps",
    )
    add_option_ini(
        "--qase-to-project",
        "qs_to_project",
        help="Project code in Qase TestOps",
    )
    add_option_ini(
        "--qase-to-run",
        "qs_to_run_id",
        help="Test Run ID in Qase TestOps",
    )
    add_option_ini(
        "--qase-to-plan",
        "qs_to_plan_id",
        help="Test Plan ID in Qase TestOps",
    )
    add_option_ini(
        "--qase-to-complete-run",
        "qs_to_complete_run",
        type="bool",
        default=False,
        help="Complete run after all tests are finished",
        action="store_false",
    )
    add_option_ini(
        "--qase-to-mode",
        "qs_to_mode",
        default="async",
        type="string",
        help="Define Qase TestOps send mode"
    )


def pytest_configure(config):
    if not hasattr(config, "workerinput"):
        QasePytestPlugin.drop_run_id()
    config.addinivalue_line("markers", "qase_id: mark test to be associate with Qase TestOps \ Report")
    config.addinivalue_line("markers", "qase_title: mark test with title")
    config.addinivalue_line("markers", "qase_description: mark test with description")

    if get_option_ini(config, "qs_mode") == 'testops':
        reporter = TestOps(
            api_token=get_option_ini(config, "qs_to_api_token"),
            project_code=get_option_ini(config, "qs_to_project"),
            run_id=get_option_ini(config, "qs_to_run_id"),
            plan_id=get_option_ini(config, "qs_to_plan_id"),
            complete_run=get_option_ini(config, "qs_to_complete_run"),
            mode=get_option_ini(config, "qs_to_mode")
        )

        QasePytestPluginSingleton.init(
            reporter=reporter
        )
        config.qaseio = QasePytestPluginSingleton.get_instance()
        config.pluginmanager.register(
            config.qaseio,
            name="qase-pytest",
        ) 


def pytest_unconfigure(config):
    qaseio = getattr(config, "src", None)
    if qaseio:
        del config.qaseio
        config.pluginmanager.unregister(qaseio)
