# -*- coding: utf-8 -*-
import functools
from contextlib import ContextDecorator as PyContextDecorator
from contextlib import _GeneratorContextManager as GeneratorContextManager
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


class ContextManager(GeneratorContextManager, PyContextDecorator):
    """Pass in a generator to the initializer and the resultant object
    is both a decorator closure and context manager
    """

    def __init__(self, func, args=(), kwargs=None):
        if kwargs is None:
            kwargs = {}

        super().__init__(func, args, kwargs)


def contextdecorator(func):
    """Similar to contextlib.contextmanager except the decorated generator
    can be used as a decorator with optional arguments.
    """

    @functools.wraps(func)
    def helper(*args, **kwargs):
        is_decorating = len(args) == 1 and callable(args[0])

        if is_decorating:
            new_func = args[0]

            @functools.wraps(new_func)
            def new_helper(*args, **kwargs):
                instance = ContextManager(func)
                return instance(new_func)(*args, **kwargs)

            return new_helper
        return ContextManager(func, args, kwargs)

    return helper


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

    @staticmethod
    @contextdecorator
    def step(identifier=None):
        """
        Step context/decorator

        Usage:

        >>> @qase.step("First step")
        ... def first_step():
        ...     print("smthng")

        >>> with qase.step("Second step"):
        ...     print("smthng")
        """
        position = None
        plugin = None
        try:
            plugin = QasePytestPluginSingleton.get_instance()
            position = plugin.start_step(identifier)
            yield
            plugin.finish_step(position)
        except Exception as e:
            if position:
                plugin.finish_step(position, exception=e)
            raise e
