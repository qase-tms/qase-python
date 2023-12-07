import concurrent.futures
import json
import logging
import os
from functools import wraps
import certifi

from qaseio.exceptions import ApiValueError
from qaseio.api_client import ApiClient
from qaseio.configuration import Configuration

QASE_ID_TAG = "qase.id"
QASE_ID_TAG_NAME = "qase.id(%d)"
QASE_TITLE_TAG_NAME = "qase.title(%s)"
ALLURE_TITLE = "@allure.title("
API_LIMIT = 100
KEEP_ALLURE_TITLE = False
MAX_NUMBER_OF_SUITES = 10000

_DEFAULT_THREAD_EXECUTOR = concurrent.futures.ThreadPoolExecutor()

logger = logging.getLogger("qaseio.utils")


class QaseClient:
    """
    Base class for Utils. All arguments are optional but for some of them like project/code or api token
    it is required that in case param is None then environment variable is set.
    """

    def __init__(self, project: str | None = None, parent_suite_id: int | None = None, token: str | None = None):
        if not project:
            project = os.getenv("QASE_TESTOPS_PROJECT")
            if not project:
                raise EnvironmentError("Set environment variable QASE_TESTOPS_PROJECT or set `project` argument")
        if not parent_suite_id:
            # parent_suite_id is optional
            parent_suite_id = os.getenv("QASE_TESTOPS_PARENT_SUITE_ID")
        if not token:
            token = os.getenv("QASE_TESTOPS_API_TOKEN")
            if not token:
                raise EnvironmentError("Set environment variable QASE_TESTOPS_API_TOKEN or set `token` argument")
        self.project = project
        self.parent_suite_id = parent_suite_id
        configuration = Configuration()
        configuration.api_key["TokenAuth"] = token
        configuration.ssl_ca_cert = certifi.where()
        self.client = ApiClient(configuration)


def threaded(f, executor=None) -> concurrent.futures.Future:
    """Decorator starting a select function in a thread.
    Returns a :py:class:`concurrent.futures.Future` object with
    task executed in a parallel executor, the default executor
    is :py:class:`concurrent.futures.ThreadPoolExecutor`.

    Usage:

    .. code-block:: py

        @threaded
        def my_concurrent_task(dev):
            res = dev.run("timeout 30 tcpdump -i eth0", timeout=60)
            return res

        # this does not block, just runs the task in a thread:
        y = my_concurrent_task(dev)
        print(y)

        # this blocks waiting for the result:
        result = y.result()  # this is how to access the actual result
        print(result)
    """

    @wraps(f)
    def wrap(*args, **kwargs):
        return (executor or _DEFAULT_THREAD_EXECUTOR).submit(f, *args, **kwargs)

    return wrap


@threaded
def call_threaded(fn, *args, **kwargs):
    return fn(*args, **kwargs)


def get_result(response, *args, **kwargs):
    result = getattr(response, "result", None)
    if not result:
        api = f"{args[0].__class__.__name__}::{kwargs}" if args else None
        raise ApiValueError(f"Unexpected response from qase_api: {api}\nresponse: {response}")
    if response.status is not True:
        raise ApiValueError(f"Unexpected response status: {response.status}")
    return result


def api_result(api_call):
    def wrapper(*args, **kwargs):
        response = api_call(*args, **kwargs)
        return get_result(response, *args, **kwargs)

    return wrapper


def json_value(api_call):
    def wrapper(*args, **kwargs):
        response = api_call(*args, **kwargs)
        result = get_result(response, *args, **kwargs)
        return json.loads(result.value)

    return wrapper
