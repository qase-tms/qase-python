# -*- coding: utf-8 -*-
from pkg_resources import DistributionNotFound, get_distribution
from typing import Tuple, Union

import pytest

from qaseio.pytest.plugin import QasePytestPluginSingleton

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = "qase-pytest"
    __version__ = get_distribution(dist_name).version
except DistributionNotFound:
    __version__ = "unknown"
finally:
    del get_distribution, DistributionNotFound


class qase:
    """Class with decorators for pytest"""

    @staticmethod
    def id(*ids):
        """
        Define the test case link to Qase TMS

        >>> @qase.id(1, 24)
        >>> def test_example():
        >>>     pass

        :param ids: int ids of test cases
        :return: pytest.mark instance
        """
        return pytest.mark.qase(ids=ids)

    @staticmethod
    def attach(*files: Union[str, Tuple[str, str], Tuple[bytes, str, str]]):
        """
        Attach files to test results

        `files` could be:
            - str - only `filepath`
            - str, str - `filepath` and `mime-type` for it
            - bytes, str, str - `source` data, `mime-type` and `filename`

        >>> from qaseio.client.models import MimeTypes
        ... qase.attach(
        ...     (driver.get_screenshot_as_png(), MimeTypes.PNG, "page.png")
        ... )
        """
        try:
            plugin = QasePytestPluginSingleton.get_instance()
            plugin.add_attachments(*files)
        except Exception:
            pass
