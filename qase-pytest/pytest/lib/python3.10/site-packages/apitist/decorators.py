import functools
from dataclasses import is_dataclass

from apitist import convclass, converter
from apitist.requests import Session
from apitist.utils import is_attrs_class


def request(method, url, **deco_kwargs):
    def _decorate(function):
        @functools.wraps(function)
        def wrapped_function(*args, **kwargs):
            result_url = url.format(*args[1:], **kwargs)
            if len(args) < 1 or function.__repr__ in dir(args[0]):
                raise Exception(
                    "You should decorate only methods of the class"
                )
            obj = args[0]
            if not getattr(obj, "session", None):
                raise Exception("Base class should define `session`")
            s: Session = getattr(obj, "session")
            modificator = function(*args, **kwargs)
            if not isinstance(modificator, dict) and modificator is not None:
                raise Exception(
                    "Modificator should be a dict of request parameters, not:",
                    modificator,
                )
            modificator = modificator if isinstance(modificator, dict) else {}
            return s.request(
                method,
                result_url,
                **modificator,
                **{
                    k: v
                    for k, v in deco_kwargs.items()
                    if k not in modificator
                },
            )

        return wrapped_function

    return _decorate


def get(url, **kwargs):
    return request("GET", url, **kwargs)


def options(url, **kwargs):
    return request("OPTIONS", url, **kwargs)


def head(url, **kwargs):
    return request("HEAD", url, **kwargs)


def post(url, **kwargs):
    return request("POST", url, **kwargs)


def put(url, **kwargs):
    return request("PUT", url, **kwargs)


def patch(url, **kwargs):
    return request("PATCH", url, **kwargs)


def delete(url, **kwargs):
    return request("DELETE", url, **kwargs)


def transform(cls):
    def to_type(self, type):
        if is_attrs_class(self):
            data = converter.unstructure(self)
            return converter.structure(data, type)
        elif is_dataclass(self):
            data = convclass.unstructure(self)
            return convclass.structure(data, type)
        raise TypeError("Object should be attrs or dataclass type")

    setattr(cls, "to_type", to_type)
    return cls
