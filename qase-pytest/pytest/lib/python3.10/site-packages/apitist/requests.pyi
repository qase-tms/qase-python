from abc import ABC
from typing import Union, Text, MutableMapping, Any, Iterable, Tuple, Optional, IO, Callable, List, TypeVar, Type

from requests import Request, Response, PreparedRequest
from requests import Session as OldSession
from requests import auth as _auth
from requests.cookies import RequestsCookieJar

DataType = TypeVar("DataType")

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


class ApitistResponse(Response):
    data: DataType
    def __init__(self, response: Response): ...
    def verify_response(self, ok_status: Union[int, List[int]] = 200) -> "ApitistResponse": ...
    def vr(self, ok_status: Union[int, List[int]] = 200) -> "ApitistResponse": ...
    def structure(self, t: Type[DataType]) -> "ApitistResponse": ...

_Data = Union[None, Text, bytes, MutableMapping[str, Any], MutableMapping[Text, Any], Iterable[Tuple[Text, Optional[Text]]], IO]

_Hook = Callable[[ApitistResponse], Any]
_Hooks = MutableMapping[Text, List[_Hook]]
_HooksInput = MutableMapping[Text, Union[Iterable[_Hook], _Hook]]
T = TypeVar("T")
R = TypeVar("R")


class Session(OldSession):
    request_hooks: List[RequestHook]
    prep_request_hooks: List[PreparedRequestHook]
    response_hooks: List[ResponseHook]
    structure_err_type: Type[T]
    base_url: str
    def __init__(self, base_url: str = None): ...
    def add_request_hook(self, hook: Type[RequestHook]): ...
    def add_prep_request_hook(self, hook: Type[PreparedRequestHook]): ...
    def add_response_hook(self, hook: Type[ResponseHook]): ...
    def add_hooks(self, *hooks: Type[Union[RequestHook, PreparedRequestHook, ResponseHook]]): ...
    def add_hook(self, hook: Type[Union[RequestHook, PreparedRequestHook, ResponseHook]]): ...
    def request(self, method: str, url: Union[str, bytes, Text],
                params: Union[None, bytes, MutableMapping[Text, Text]] = ...,
                data: _Data = ...,
                headers: Optional[MutableMapping[Text, Text]] = ...,
                cookies: Union[None, RequestsCookieJar, MutableMapping[Text, Text]] = ...,
                files: Optional[MutableMapping[Text, IO[Any]]] = ...,
                auth: Union[None, Tuple[Text, Text], _auth.AuthBase, Callable[[Request], Request]] = ...,
                timeout: Union[None, float, Tuple[float, float], Tuple[float, None]] = ...,
                allow_redirects: Optional[bool] = ...,
                proxies: Optional[MutableMapping[Text, Text]] = ...,
                hooks: Optional[_HooksInput] = ...,
                stream: Optional[bool] = ...,
                verify: Union[None, bool, Text] = ...,
                cert: Union[Text, Tuple[Text, Text], None] = ...,
                json: Optional[Any] = ...,
                structure_type: Optional[R] = ...,
                structure_err_type: Optional[T] = ...,
                name: str = ...,
                ) -> ApitistResponse: ...
    def get(self, url: Union[Text, bytes], **kwargs) -> ApitistResponse: ...
    def options(self, url: Union[Text, bytes], **kwargs) -> ApitistResponse: ...
    def head(self, url: Union[Text, bytes], **kwargs) -> ApitistResponse: ...
    def post(self, url: Union[Text, bytes], data: _Data = ..., json: Optional[Any] = ..., **kwargs) -> ApitistResponse: ...
    def put(self, url: Union[Text, bytes], data: _Data = ..., **kwargs) -> ApitistResponse: ...
    def patch(self, url: Union[Text, bytes], data: _Data = ..., **kwargs) -> ApitistResponse: ...
    def delete(self, url: Union[Text, bytes], **kwargs) -> ApitistResponse: ...


class SharedSession:
    def __init__(self, *sessions: OldSession): ...
    def add_sessions(self, *sessions: OldSession): ...
    def validate_sessions(self): ...
    def synchronize_sessions(self): ...

def session(base_url: str = None) -> Session: ...
