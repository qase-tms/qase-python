import sys
from pathlib import Path
from unittest.mock import MagicMock

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib

from qase.tavern import conftest


def test_pytest11_entry_point_does_not_clash_with_qase_pytest():
    # pytest loads only one plugin per entry-point name, so sharing
    # "qase_pytest" with qase-pytest silently disables one of the two packages.
    pyproject = Path(__file__).resolve().parents[1] / "pyproject.toml"
    data = tomllib.loads(pyproject.read_text())

    entry_points = data["project"]["entry-points"]["pytest11"]

    assert entry_points == {"qase_tavern": "qase.tavern.conftest"}


def test_unconfigure_unregisters_plugin():
    plugin = object()
    config = MagicMock()
    config.qase = plugin

    conftest.pytest_unconfigure(config)

    config.pluginmanager.unregister.assert_called_once_with(plugin)
    assert not hasattr(config, "qase")
