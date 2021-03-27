from typing import Callable, List, Type, TypeVar, Union

import attr
from apitist.constructor import converter
from apitist.requests import Session
from requests import Response


class BadRequestException(Exception):
    pass


class UnauthorizedException(Exception):
    pass


class ForbiddenException(Exception):
    pass


class NotFoundException(Exception):
    pass


class TooManyRequestsException(Exception):
    pass


exceptions = {
    400: BadRequestException,
    401: UnauthorizedException,
    403: ForbiddenException,
    404: NotFoundException,
    429: TooManyRequestsException,
}


T = TypeVar("T")


@attr.s
class BaseService:
    s: Session = attr.ib()
    path: Callable[[str], str] = attr.ib()
    _in_test = attr.ib(default=False)
    _last_res = attr.ib(default=False)

    def validate_response(
        self,
        res: Response,
        to_type: Type[T],
        status: Union[int, List[int]] = 200,
    ) -> T:
        if isinstance(status, int):
            status = [status]

        if self._in_test:
            self._last_res = res

        if res.status_code in exceptions:
            message = "Got error during response: {}".format(res.content)
            raise exceptions[res.status_code](message)

        if res.status_code not in status:
            raise ValueError(
                "Got unexpected status code: {} {}".format(
                    res.status_code, res.content
                )
            )
        try:
            data = res.json()
            if data.get("status") is True and to_type:
                return converter.structure(data.get("result"), to_type)
            elif data.get("status") is True:
                return data.get("result")
        except Exception as e:
            raise ValueError("Unable to parse response {}".format(e))
        raise ValueError("Got error during response: {}".format(res.content))

    vr = validate_response
