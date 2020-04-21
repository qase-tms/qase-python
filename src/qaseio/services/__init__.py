from typing import Callable

import attr
from apitist.requests import Session
from requests import Response


@attr.s
class BaseService:
    s: Session = attr.ib()
    path: Callable[[str], str] = attr.ib()

    @staticmethod
    def validate_response(res: Response):
        if res.status_code != 200:
            res.raise_for_status()
        try:
            data = res.json()
            if data.get("status") is True:
                return data.get("result")
        except Exception as e:
            raise ValueError("Unable to parse response {}".format(e))
        raise ValueError("Got error during response: {}", res.content)

    vr = validate_response

