from functools import partial
from typing import Callable
from urllib.parse import urljoin

import attr
from apitist.hooks import (
    PrepRequestDebugLoggingHook,
    RequestConverterHook,
    ResponseDebugLoggingHook,
)
from apitist.requests import Session

from qaseio.services.projects import Projects
from qaseio.services.runs import Runs
from qaseio.services.test_cases import TestCases


@attr.s
class Client:
    api_token: str = attr.ib(repr=False)
    _s: Session = attr.ib(factory=lambda: Session(), repr=False, init=False)
    _path: Callable[[str], str] = attr.ib(repr=False, init=False)
    projects: Projects = attr.ib(init=False)
    test_cases: TestCases = attr.ib(init=False)
    runs: Runs = attr.ib(init=False)

    def __attrs_post_init__(self):
        self._s.add_request_hook(RequestConverterHook)
        self._s.add_prep_request_hook(PrepRequestDebugLoggingHook)
        self._s.add_response_hook(ResponseDebugLoggingHook)
        self._s.headers.update({"Token": self.api_token})

        def get_url(path: str):
            if isinstance(path, str) and path.startswith("/"):
                path = path[1:]
            return partial(urljoin, "https://api.qase.io/v1/")(path)

        self._path = get_url

        self.projects = Projects(self._s, self._path)
        self.test_cases = TestCases(self._s, self._path)
        self.runs = Runs(self._s, self._path)
