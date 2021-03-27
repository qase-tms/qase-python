from qaseio.pytest.plugin import QasePytestPluginSingleton


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
        "--qase",
        "qs_enabled",
        default=False,
        type="bool",
        help="Use Qase TMS",
        action="store_true",
    )
    add_option_ini(
        "--qase-api-token",
        "qs_api_token",
        help="Api token for Qase TMS",
    )
    add_option_ini(
        "--qase-project",
        "qs_project_code",
        help="Project code in Qase TMS",
    )
    add_option_ini(
        "--qase-testrun",
        "qs_testrun_id",
        help="Testrun ID in Qase TMS",
    )
    add_option_ini(
        "--qase-testplan",
        "qs_testplan_id",
        help="Testplan ID in Qase TMS",
    )
    add_option_ini(
        "--qase-new-run",
        "qs_new_run",
        default=False,
        type="bool",
        help="Create new testrun, if no testrun id provided",
        action="store_true",
    )
    add_option_ini(
        "--qase-debug",
        "qs_debug",
        default=False,
        type="bool",
        help="Prints additional output of plugin",
        action="store_true",
    )


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "qase(*ids): mark test to be associate with Qase TMS"
    )
    if get_option_ini(config, "qs_enabled"):
        QasePytestPluginSingleton.init(
            api_token=get_option_ini(config, "qs_api_token"),
            project=get_option_ini(config, "qs_project_code"),
            testrun=get_option_ini(config, "qs_testrun_id"),
            testplan=get_option_ini(config, "qs_testplan_id"),
            create_run=get_option_ini(config, "qs_new_run"),
            debug=get_option_ini(config, "qs_debug"),
        )
        config.pluginmanager.register(
            QasePytestPluginSingleton.get_instance(),
            name="qase-pytest",
        )
