from .plugin import QasePytestPlugin, QasePytestPluginSingleton

from qase.commons.reporters import QaseCoreReporter

from .options import QasePytestOptions
from qase.commons.config import ConfigManager


def pytest_addoption(parser):
    group = parser.getgroup("qase")
    QasePytestOptions.addoptions(parser, group)


def pytest_configure(config):
    config = _add_markers(config)

    config_manager = setup_config_manager(config)

    QasePytestPluginSingleton.init(reporter=QaseCoreReporter(config_manager))
    config.qase = QasePytestPluginSingleton.get_instance()
    config.pluginmanager.register(
        config.qase,
        name="qase-pytest",
    )


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


def setup_config_manager(config):
    config_manager = ConfigManager()
    for option in config.option.__dict__:
        if option.startswith("qase_") and option and config.option.__dict__[option] is not None:
            config_manager.set(option.replace("qase_", "").replace("_", "."), config.option.__dict__[option])
    return config_manager


def pytest_unconfigure(config):
    qase = getattr(config, "src", None)
    if qase:
        del config.qase
        config.pluginmanager.unregister(qase)
