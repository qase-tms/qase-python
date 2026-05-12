"""Native pytest-bdd integration for qase-pytest.

Loaded conditionally from conftest.py only when pytest_bdd is installed.
"""


class QasePytestBddPlugin:
    """Bridge between pytest-bdd hooks and the main QasePytestPlugin runtime."""

    def __init__(self, pytest_plugin):
        self._pytest_plugin = pytest_plugin
