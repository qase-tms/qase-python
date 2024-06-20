import sys
from typing import List

if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing import Dict as TypedDict


class StartSuiteModel(TypedDict):
    id: str
    longname: str
    doc: str
    metadata: dict
    source: str
    suites: List[str]
    tests: List[str]
    totaltests: int
    starttime: str


class EndSuiteModel(TypedDict):
    id: str
    longname: str
    doc: str
    metadata: dict
    source: str
    starttime: str
    endtime: str
    elapsedtime: int
    status: str
    statistics: str
    message: str


class StartTestModel(TypedDict):
    id: str
    longname: str
    originalname: str
    doc: dict
    tags: List[str]
    critical: str
    template: str
    lineno: int
    starttime: str


class EndTestModel(TypedDict):
    id: str
    longname: str
    originalname: str
    doc: dict
    tags: List[str]
    critical: str
    template: str
    lineno: int
    starttime: str
    endtime: str
    elapsedtime: int
    status: str
    message: str
    source: str


class StartKeywordModel(TypedDict):
    type: str
    kwname: str
    libname: str
    doc: dict
    args: List[str]
    assign: List[str]
    tags: List[str]
    starttime: str


class EndKeywordModel(TypedDict):
    type: str
    kwname: str
    libname: str
    doc: dict
    args: List[str]
    assign: List[str]
    tags: List[str]
    starttime: str
    endtime: str
    elapsedtime: int
    status: str
