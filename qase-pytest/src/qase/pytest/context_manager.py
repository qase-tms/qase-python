# -*- coding: utf-8 -*-
import functools
from contextlib import ContextDecorator as PyContextDecorator
from contextlib import _GeneratorContextManager as GeneratorContextManager


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
