import pytest

import attr
from requests import Response

from qaseio.models import ProjectCreated
from qaseio.services import BaseService, TooManyRequestsException


@pytest.mark.parametrize("values", [(), (None,)])
def test_empty_service_init(values):
    with pytest.raises(TypeError):
        BaseService(*values)


def test_vr_too_many_requests():
    res = Response()
    res.status_code = 429
    res._content = b'{"status":true,"result":{}}'
    with pytest.raises(TooManyRequestsException):
        BaseService.validate_response(res, to_type=None)


@pytest.mark.parametrize(
    "res_status, validate_status", [(201, 201), (202, [200, 201, 202])]
)
def test_vr_correct_status_code(res_status, validate_status):
    res = Response()
    res.status_code = res_status
    res._content = b'{"status":true,"result":{}}'
    data = BaseService.validate_response(
        res, to_type=None, status=validate_status
    )
    assert data == {}


@pytest.mark.parametrize(
    "res_status, validate_status", [(201, 20), (203, [200, 201, 202])]
)
def test_vr_incorrect_status_code(res_status, validate_status):
    res = Response()
    res.status_code = res_status
    res._content = b'{"status":true,"result":{}}'
    with pytest.raises(ValueError):
        BaseService.validate_response(
            res, to_type=None, status=validate_status
        )


def test_vr_res_status_false():
    res = Response()
    res.status_code = 200
    res._content = b'{"status":false,"result":{}}'
    with pytest.raises(ValueError):
        BaseService.validate_response(res, to_type=None)


def test_vr_res_not_json():
    res = Response()
    res.status_code = 200
    res._content = b"some none json string"
    with pytest.raises(ValueError):
        BaseService.validate_response(res, to_type=None)


def test_vr_res_correct_type():
    res = Response()
    res.status_code = 200
    res._content = b'{"status":true,"result":{"code":"TRU"}}'
    data = BaseService.validate_response(res, to_type=ProjectCreated)
    assert isinstance(data, ProjectCreated)
    assert data.code == "TRU"


def test_vr_res_incorrect_type():
    @attr.s
    class Ex:
        field = attr.ib()

    res = Response()
    res.status_code = 200
    res._content = b'{"status":true,"result":{"codes":"TRU"}}'
    with pytest.raises(ValueError):
        BaseService.validate_response(res, to_type=Ex)
