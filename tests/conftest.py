import pytest

from qaseio import QaseApi
from qaseio.services import BaseService


@pytest.fixture()
def client():
    api = QaseApi("")
    api.projects._in_test = True
    api.test_cases._in_test = True
    api.runs._in_test = True
    return api


@pytest.fixture()
def base_service():
    return BaseService(None, None)
