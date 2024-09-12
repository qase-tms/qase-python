import sys
import threading
import uuid
from functools import wraps
from ..models.runtime import Runtime
from ..models.step import Step, StepRequestData, StepType


class NetworkProfiler:
    _instance = None

    def __init__(self, runtime: Runtime, skip_domain: str, track_on_fail: bool = True):
        self._original_functions = {}
        self.runtime = runtime
        self.skip_domain = skip_domain
        self.track_on_fail = track_on_fail
        self.step = None

    def enable(self):
        if 'requests' in sys.modules:
            import requests
            self._original_functions['requests'] = requests.Session.send
            requests.Session.send = self._requests_send_wrapper(requests.Session.send)

        if 'urllib3' in sys.modules:
            import urllib3
            self._original_functions['urllib3'] = urllib3.PoolManager.request
            urllib3.PoolManager.request = self._urllib3_request_wrapper(urllib3.PoolManager.request)

    def disable(self):
        if 'requests' in self._original_functions:
            import requests
            requests.Session.send = self._original_functions['requests']

        if 'urllib3' in self._original_functions:
            import urllib3
            urllib3.PoolManager.request = self._original_functions['urllib3']

    def _requests_send_wrapper(self, func):
        @wraps(func)
        def wrapper(self, request, *args, **kwargs):
            NetworkProfilerSingleton.get_instance()._log_request(request)
            response = func(self, request, *args, **kwargs)
            NetworkProfilerSingleton.get_instance()._log_response(response)
            return response

        return wrapper

    def _urllib3_request_wrapper(self, func):
        skip_domain = self.skip_domain

        @wraps(func)
        def wrapper(self, method, url, *args, **kwargs):
            if skip_domain in url:
                return func(self, method, url, *args, **kwargs)

            interceptor = NetworkProfilerSingleton.get_instance()
            request = lambda: None
            request.method = method
            request.url = url

            interceptor._log_request(request)
            response = func(self, method, url, *args, **kwargs)
            interceptor._log_response(response, url=url)
            return response

        return wrapper

    @staticmethod
    def _log_request(request):
        NetworkProfilerSingleton.get_instance().step = Step(
            id=str(uuid.uuid4()),
            step_type=StepType.REQUEST,
            data=StepRequestData(
                request_method=request.method,
                request_url=request.url,
                request_body=request.body if hasattr(request, 'body') else None,
                request_headers=request.headers if hasattr(request, 'headers') else None
            ),
        )

    @staticmethod
    def _log_response(response, url=None, *args, **kwargs):
        status = response.status if hasattr(response, 'status') else response.status_code
        profiler = NetworkProfilerSingleton.get_instance()
        if profiler.step is None:
            profiler.step = Step(
                id=str(uuid.uuid4()),
                step_type=StepType.REQUEST,
                data=StepRequestData(
                    request_method=response.request.method,
                    request_url=response.request.url,
                    request_body=response.request.body if hasattr(response.request, 'body') else None,
                    request_headers=response.request.headers if hasattr(response.request, 'headers') else None
                ))
        profiler.step.data.add_response(
            status_code=status,
            response_body=str(response.data if hasattr(response,
                                                       'data') else response.content) if profiler.track_on_fail and status >= 400 else None,
            response_headers=response.headers if profiler.track_on_fail and status >= 400 else None,
        )
        profiler.runtime.add_step(profiler.step)
        profiler.runtime.finish_step(
            id=profiler.step.id,
            status='passed' if status < 400 else 'failed',
        )
        profiler.step = None


class NetworkProfilerSingleton:
    _instance = None
    _lock = threading.Lock()

    @staticmethod
    def init(**kwargs):
        if NetworkProfilerSingleton._instance is None:
            with NetworkProfilerSingleton._lock:
                if NetworkProfilerSingleton._instance is None:
                    NetworkProfilerSingleton._instance = NetworkProfiler(**kwargs)

    @staticmethod
    def get_instance() -> NetworkProfiler:
        """ Static access method"""
        if NetworkProfilerSingleton._instance is None:
            raise Exception("Init plugin first")
        return NetworkProfilerSingleton._instance

    def __init__(self):
        """ Virtually private constructor"""
        raise Exception("Use get_instance()")
