# -*- coding: utf-8 -*-
from pkg_resources import DistributionNotFound, get_distribution

import pytest

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
