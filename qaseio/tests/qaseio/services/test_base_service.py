import pytest

import attr
from requests import Response

from qaseio.client.models import ProjectCreated
from qaseio.client.services import BaseService, TooManyRequestsException


@pytest.mark.parametrize("values", [(), (None,)])
def test_empty_service_init(values):
    with pytest.raises(TypeError):
        BaseService(*values)


def test_vr_too_many_requests(base_service):
    res = Response()
    res.status_code = 429
    res._content = b'{"status":true,"result":{}}'
    with pytest.raises(TooManyRequestsException):
        base_service.validate_response(res, to_type=None)


@pytest.mark.parametrize(
    "res_status, validate_status", [(201, 201), (202, [200, 201, 202])]
)
def test_vr_correct_status_code(base_service, res_status, validate_status):
    res = Response()
    res.status_code = res_status
    res._content = b'{"status":true,"result":{}}'
    data = base_service.validate_response(
        res, to_type=None, status=validate_status
    )
    assert data == {}


@pytest.mark.parametrize(
    "res_status, validate_status", [(201, 20), (203, [200, 201, 202])]
)
def test_vr_incorrect_status_code(base_service, res_status, validate_status):
    res = Response()
    res.status_code = res_status
    res._content = b'{"status":true,"result":{}}'
    with pytest.raises(ValueError):
        base_service.validate_response(
            res, to_type=None, status=validate_status
        )


def test_vr_res_status_false(base_service):
    res = Response()
    res.status_code = 200
    res._content = b'{"status":false,"result":{}}'
    with pytest.raises(ValueError):
        base_service.validate_response(res, to_type=None)


def test_vr_res_not_json(base_service):
    res = Response()
    res.status_code = 200
    res._content = b"some none json string"
    with pytest.raises(ValueError):
        base_service.validate_response(res, to_type=None)


def test_vr_res_correct_type(base_service):
    res = Response()
    res.status_code = 200
    res._content = b'{"status":true,"result":{"code":"TRU"}}'
    data = base_service.validate_response(res, to_type=ProjectCreated)
    assert isinstance(data, ProjectCreated)
    assert data.code == "TRU"


def test_vr_res_incorrect_type(base_service):
    @attr.s
    class Ex:
        field = attr.ib()

    res = Response()
    res.status_code = 200
    res._content = b'{"status":true,"result":{"codes":"TRU"}}'
    with pytest.raises(ValueError):
        base_service.validate_response(res, to_type=Ex)
