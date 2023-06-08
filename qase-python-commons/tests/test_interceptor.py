import sys
import unittest
import urllib3
import requests
from unittest.mock import Mock, patch, call
from qaseio.commons.models.runtime import Runtime
from qaseio.commons.models.step import Step, StepRequestData
from qaseio.commons.interceptor import Interceptor, InterceptorSingleton  # replace 'your_module' with the actual module name

class TestInterceptor(unittest.TestCase):
    def setUp(self):
        self.runtime = Runtime()
        self.interceptor = Interceptor(runtime=self.runtime)
        self.requests_send = Mock()
        self.urllib3_request = Mock()

    def tearDown(self):
        self.interceptor.disable()

    @patch('sys.modules', new_callable=dict)
    def test_apply_wrappers_requests(self, sys_modules):
        sys_modules.update({'requests': Mock()})
        with patch.object(self.interceptor, '_requests_send_wrapper', return_value=self.requests_send):
            self.interceptor.enable()
            self.assertEqual(sys.modules['requests'].Session.send, self.requests_send)

    @patch('sys.modules', new_callable=dict)
    def test_apply_wrappers_urllib3(self, sys_modules):
        sys_modules.update({'urllib3': Mock()})
        with patch.object(self.interceptor, '_urllib3_request_wrapper', return_value=self.urllib3_request):
            self.interceptor.enable()
            self.assertEqual(sys.modules['urllib3'].PoolManager.request, self.urllib3_request)

    @patch('sys.modules', new_callable=dict)
    def test_remove_wrappers_requests(self, sys_modules):
        sys_modules.update({'requests': self.requests_send})
        self.interceptor._original_functions['requests'] = self.requests_send
        self.interceptor.disable()
        self.assertEqual(sys.modules['requests'].Session.send, self.requests_send)

    @patch('sys.modules', new_callable=dict)
    def test_remove_wrappers_urllib3(self, sys_modules):
        sys_modules.update({'urllib3': self.urllib3_request})
        self.interceptor._original_functions['urllib3'] = self.urllib3_request
        self.interceptor.disable()
        self.assertEqual(sys.modules['urllib3'].PoolManager.request, self.urllib3_request)

    @patch.object(InterceptorSingleton, 'get_instance')
    @patch.object(Interceptor, '_log_pre_request')
    @patch.object(Interceptor, '_log_post_response')
    def test_requests_send_wrapper(self, log_post_mock, log_pre_mock, get_instance_mock):
        get_instance_mock.return_value = self.interceptor
        request_mock = Mock(method='GET', url='http://test.com', body=None, headers=None)
        response_mock = Mock(status_code=200, content='OK', headers=None)
        self.requests_send.return_value = response_mock

        wrapper = self.interceptor._requests_send_wrapper(self.requests_send)
        response = wrapper(request_mock)

        self.assertEqual(response, response_mock)
        log_pre_mock.assert_called_once_with(request_mock)
        log_post_mock.assert_called_once_with(response_mock)

    @patch.object(InterceptorSingleton, 'get_instance')
    @patch.object(Interceptor, '_log_pre_request')
    @patch.object(Interceptor, '_log_post_response')
    def test_urllib3_request_wrapper(self, log_post_mock, log_pre_mock, get_instance_mock):
        get_instance_mock.return_value = self.interceptor
        response_mock = Mock(status=200, data='OK', headers=None)
        self.urllib3_request.return_value = response_mock

        wrapper = self.interceptor._urllib3_request_wrapper(self.urllib3_request)
        response = wrapper('GET', 'http://test.com')

        self.assertEqual(response, response_mock)
        request = log_pre_mock.call_args[0][0]
        self.assertEqual(request.method, 'GET')
        self.assertEqual(request.url, 'http://test.com')
        log_post_mock.assert_called_once_with(response_mock, url='http://test.com')

    @patch.object(InterceptorSingleton, 'get_instance')
    @patch.object(StepRequestData, '__init__', return_value=None)
    @patch.object(Step, '__init__', return_value=None)
    def test_log_pre_request(self, step_init_mock, request_data_init_mock, get_instance_mock):
        interceptor_mock = Mock(spec=Interceptor)
        get_instance_mock.return_value = interceptor_mock
        request_mock = Mock(method='GET', url='http://test.com', body=None, headers=None)
        Interceptor._log_pre_request(request_mock)

        request_data_init_mock.assert_called_once_with(
            request_method=request_mock.method,
            request_url=request_mock.url,
            request_body=request_mock.body,
            request_headers=request_mock.headers,
        )
        step_init_mock.assert_called_once_with(id=mock.ANY, step_type='request', data=mock.ANY)
        self.assertIsNotNone(interceptor_mock.step)

    @patch.object(InterceptorSingleton, 'get_instance')
    def test_log_post_response(self, get_instance_mock):
        interceptor_mock = Mock(spec=Interceptor)
        get_instance_mock.return_value = interceptor_mock
        response_mock = Mock(status=200, data='OK', headers=None)
        Interceptor._log_post_response(response_mock, url='http://test.com')

        interceptor_mock.step.data.add_response.assert_called_once_with(
            status_code=response_mock.status,
            response_body=str(response_mock.data) if interceptor_mock.track_on_fail and response_mock.status >= 400 else None,
            response_headers=response_mock.headers if interceptor_mock.track_on_fail and response_mock.status >= 400 else None,
        )
        interceptor_mock.runtime.add_step.assert_called_once_with(interceptor_mock.step)
        interceptor_mock.runtime.finish_step.assert_called_once_with(
            id=interceptor_mock.step.id,
            status='passed' if response_mock.status < 400 else 'failed',
        )
        self.assertIsNone(interceptor_mock.step)

class TestInterceptorSingleton(unittest.TestCase):
    @patch.object(InterceptorSingleton, '__init__', return_value=None)
    def setUp(self, init_mock):
        self.interceptor = InterceptorSingleton()
        self.runtime = Runtime()
        InterceptorSingleton._instance = None

    def test_init(self):
        self.assertIsNone(InterceptorSingleton._instance)
        InterceptorSingleton.init(runtime=self.runtime)
        self.assertIsInstance(InterceptorSingleton._instance, Interceptor)

    def test_get_instance(self):
        InterceptorSingleton.init(runtime=self.runtime)
        self.assertEqual(InterceptorSingleton.get_instance(), InterceptorSingleton._instance)

    def test_get_instance_no_init(self):
        with self.assertRaises(Exception):
            InterceptorSingleton.get_instance()
            
if __name__ == '__main__':
    unittest.main()