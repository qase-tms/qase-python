"""Tests for the pytest-bdd bridge plugin (QasePytestBddPlugin)."""

import pytest


def test_bdd_module_importable():
    """The bdd module exists and can be imported without pytest_bdd present at runtime."""
    from qase.pytest import bdd as bdd_module
    assert hasattr(bdd_module, "QasePytestBddPlugin")


def test_bdd_plugin_constructs_with_pytest_plugin():
    """QasePytestBddPlugin can be instantiated by passing a pytest plugin instance."""
    from qase.pytest.bdd import QasePytestBddPlugin
    fake_pytest_plugin = object()
    plugin = QasePytestBddPlugin(fake_pytest_plugin)
    assert plugin is not None
