import inspect
from abc import ABC
from typing import List, Set, Type, TypeVar, Union
from urllib.parse import urlparse

from requests import HTTPError, PreparedRequest, Request, Response
from requests import Session as OldSession
from requests.cookies import cookiejar_from_dict, merge_cookies

from apitist.logging import Logging


class SessionHook(ABC):
    pass


class RequestHook(SessionHook):
    def run(self, request: Request) -> Request:
        ...


class PreparedRequestHook(SessionHook):
    def run(self, request: PreparedRequest) -> PreparedRequest:
        ...


class ResponseHook(SessionHook):
    def run(self, response: Response) -> Response:
        ...


class ResponseCoverterHook(SessionHook):
    def run(self, response: Response) -> Response:
        ...


DataType = TypeVar("DataType")


class ApitistResponse(Response):
    data: DataType

    def __init__(self, response: Response):
        self.__dict__ = response.__dict__

    def verify_response(
        self, ok_status: Union[int, List[int]] = 200
    ) -> "ApitistResponse":
        func = inspect.stack()[2][3]
        if isinstance(ok_status, int):
            ok_status = [ok_status]
        if self.status_code not in ok_status:
            raise ValueError(
                f"Verified response: function {func} failed: "
                f"server responded {self.status_code} "
                f"with data: {self.content}"
            )
        else:
            Logging.logger.info(
                f"Verified response: function {func} code {self.status_code}"
            )
        return self

    def vr(self, ok_status: Union[int, List[int]] = 200) -> "ApitistResponse":
        return self.verify_response(ok_status=ok_status)

    def structure(self, t: Type[DataType]) -> "ApitistResponse":
        ...


T = TypeVar("T")


class Session(OldSession):
    def __init__(
        self, base_url: str = None, structure_err_type: Type[T] = None
    ):
        super().__init__()
        self.request_hooks = []
        self.prep_request_hooks = []
        self.response_hooks = []
        self.base_url = base_url
        self.structure_err_type = structure_err_type

    def _add_hook(
        self,
        hook: Type[Union[RequestHook, PreparedRequestHook, ResponseHook]],
        array: list,
    ):
        array.append(hook)

    def add_request_hook(self, hook: Type[RequestHook]):
        Logging.logger.debug("Adding new request hook")
        self._add_hook(hook, self.request_hooks)

    def add_prep_request_hook(self, hook: Type[PreparedRequestHook]):
        Logging.logger.debug("Adding new prepared request hook")
        self._add_hook(hook, self.prep_request_hooks)

    def add_response_hook(self, hook: Type[ResponseHook]):
        Logging.logger.debug("Adding new response hook")
        self._add_hook(hook, self.response_hooks)

    def add_hooks(
        self,
        *hooks: Type[Union[RequestHook, PreparedRequestHook, ResponseHook]],
    ):
        for hook in hooks:
            self.add_hook(hook)

    def add_hook(
        self, hook: Type[Union[RequestHook, PreparedRequestHook, ResponseHook]]
    ):
        if issubclass(hook, RequestHook):
            self.add_request_hook(hook)
        elif issubclass(hook, PreparedRequestHook):
            self.add_prep_request_hook(hook)
        elif issubclass(hook, ResponseHook):
            self.add_response_hook(hook)

    def _run_hooks(
        self,
        array: List[
            Type[Union[RequestHook, PreparedRequestHook, ResponseHook]]
        ],
        data: Union[Request, PreparedRequest, Response, ApitistResponse],
    ):
        for hook in array:
            data = hook().run(data)
        return data

    def _structure_response(
        self, response: Response, structure_type, structure_err_type
    ) -> Union[ApitistResponse, Response]:
        if not getattr(response, "structure", None):
            return response

        try:
            json = response.json()
        except ValueError:
            json = None

        if not json:
            return response

        try:
            response.raise_for_status()
            if structure_type is not None:
                response = response.structure(structure_type)
        except HTTPError:
            if structure_err_type is not None:
                response = response.structure(structure_err_type)
        return response

    def request(
        self,
        method,
        url,
        params=None,
        data=None,
        headers=None,
        cookies=None,
        files=None,
        auth=None,
        timeout=None,
        allow_redirects=True,
        proxies=None,
        hooks=None,
        stream=None,
        verify=None,
        cert=None,
        json=None,
        structure_type=None,
        structure_err_type=None,
        name=None,
    ) -> ApitistResponse:
        """Constructs a :class:`Request <Request>`, prepares it and sends it.
        Returns :class:`Response <Response>` object.

        :param method: method for the new :class:`Request` object.
        :param url: URL for the new :class:`Request` object.
        :param params: (optional) Dictionary or bytes to be sent in the query
            string for the :class:`Request`.
        :param data: (optional) Dictionary, list of tuples, bytes, or file-like
            object to send in the body of the :class:`Request`.
        :param json: (optional) json to send in the body of the
            :class:`Request`.
        :param headers: (optional) Dictionary of HTTP Headers to send with the
            :class:`Request`.
        :param cookies: (optional) Dict or CookieJar object to send with the
            :class:`Request`.
        :param files: (optional) Dictionary of ``'filename':
            file-like-objects`` for multipart encoding upload.
        :param auth: (optional) Auth tuple or callable to enable
            Basic/Digest/Custom HTTP Auth.
        :param timeout: (optional) How long to wait for the server to send
            data before giving up, as a float, or a :ref:`(connect timeout,
            read timeout) <timeouts>` tuple.
        :type timeout: float or tuple
        :param allow_redirects: (optional) Set to True by default.
        :type allow_redirects: bool
        :param proxies: (optional) Dictionary mapping protocol or protocol and
            hostname to the URL of the proxy.
        :param stream: (optional) whether to immediately download the response
            content. Defaults to ``False``.
        :param verify: (optional) Either a boolean, in which case it controls
            whether we verify the server's TLS certificate, or a string,
            in which case it must be a path to a CA bundle to use.
            Defaults to ``True``.
        :param cert: (optional) if String, path to ssl client cert file (.pem).
            If Tuple, ('cert', 'key') pair.
        :param structure_type: (optional) Type which would be used to structure
            json response
        :param structure_err_type: (optional) Type which would be used to
            structure json response, if response status is not 2xx
        :param name: (optional) Human-readable description
        :rtype: requests.Response
        """
        # Create the Request.
        parsed_url = urlparse(url)
        if parsed_url.scheme and parsed_url.hostname:
            result_url = url
        else:
            result_url = "/".join([self.base_url.rstrip("/"), url.lstrip("/")])
        req = Request(
            method=method.upper(),
            url=result_url,
            headers=headers,
            files=files,
            data=data or {},
            json=json,
            params=params or {},
            auth=auth,
            cookies=cookies,
            hooks=hooks,
        )
        setattr(req, "name", name)
        req = self._run_hooks(self.request_hooks, req)
        prep = self.prepare_request(req)
        setattr(prep, "name", name)
        prep = self._run_hooks(self.prep_request_hooks, prep)

        proxies = proxies or {}

        settings = self.merge_environment_settings(
            prep.url, proxies, stream, verify, cert
        )

        # Send the request.
        send_kwargs = {"timeout": timeout, "allow_redirects": allow_redirects}
        send_kwargs.update(settings)
        resp = ApitistResponse(self.send(prep, **send_kwargs))
        setattr(resp, "name", name)
        resp = self._run_hooks(self.response_hooks, resp)

        self._structure_response(
            resp, structure_type, structure_err_type or self.structure_err_type
        )

        return resp


class SharedSession:
    """
    Class to synchronize cookies between different sessions.
    On each completed response cookies are merged between
    all registered session objects
    """

    def __init__(self, *sessions: OldSession):
        self._shared_state = {"cookies": cookiejar_from_dict({})}
        self._sessions: Set[OldSession] = set()

        class SharedSessionHook(ResponseHook):
            def run(cls, response: Response) -> Response:
                nonlocal self
                self.synchronize_sessions()
                return response

        self._hook = SharedSessionHook
        self.add_sessions(*sessions)

    def add_sessions(self, *sessions: OldSession):
        self._sessions.update(sessions)
        self.validate_sessions()
        self._register_hooks()

    def validate_sessions(self):
        for s in self._sessions:
            if not isinstance(s, OldSession):
                raise ValueError(
                    "Session should be an instance of `Session` "
                    "from apitist package"
                )

    def synchronize_sessions(self):
        for s in self._sessions:
            self._shared_state["cookies"] = merge_cookies(
                self._shared_state["cookies"], s.cookies
            )
            s.cookies = self._shared_state["cookies"]

    def _register_hooks(self):
        for s in self._sessions:
            if self._hook not in s.response_hooks:
                s.add_hook(self._hook)


def session(base_url: str = None):
    """
    Returns a :class:`Session` for context-management.

    :rtype: Session
    """
    return Session(base_url=base_url)
