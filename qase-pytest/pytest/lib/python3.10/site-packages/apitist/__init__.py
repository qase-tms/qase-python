"""Apitist package"""
from pkg_resources import DistributionNotFound, get_distribution

from .constructor import (
    AttrsConverter,
    Converter,
    ConverterType,
    DataclassConverter,
    convclass,
    converter,
)
from .hooks import (
    PreparedRequestHook,
    PrepRequestDebugLoggingHook,
    PrepRequestInfoLoggingHook,
    RequestAttrsConverterHook,
    RequestConverterHook,
    RequestDataclassConverterHook,
    RequestDebugLoggingHook,
    RequestHook,
    RequestInfoLoggingHook,
    ResponseAttrsConverterHook,
    ResponseConverterHook,
    ResponseDataclassConverterHook,
    ResponseDebugLoggingHook,
    ResponseHook,
    ResponseInfoLoggingHook,
    request_converter_hook,
    response_converter_hook,
)
from .random import Randomer
from .requests import Session, SharedSession, session

__all__ = [
    "__version__",
    "dist_name",
    "AttrsConverter",
    "DataclassConverter",
    "convclass",
    "converter",
    "ConverterType",
    "Converter",
    "PreparedRequestHook",
    "PrepRequestDebugLoggingHook",
    "PrepRequestInfoLoggingHook",
    "RequestAttrsConverterHook",
    "RequestConverterHook",
    "RequestDataclassConverterHook",
    "RequestDebugLoggingHook",
    "RequestHook",
    "RequestInfoLoggingHook",
    "ResponseAttrsConverterHook",
    "ResponseConverterHook",
    "ResponseDataclassConverterHook",
    "ResponseDebugLoggingHook",
    "ResponseHook",
    "ResponseInfoLoggingHook",
    "Randomer",
    "session",
    "Session",
    "SharedSession",
    "request_converter_hook",
    "response_converter_hook",
]

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = "apitist"
    __version__ = get_distribution(dist_name).version
except DistributionNotFound as e:
    __version__ = "unknown"
    print(e)
finally:
    del get_distribution, DistributionNotFound
