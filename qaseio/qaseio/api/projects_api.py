"""
    Qase.io API

    Qase API Specification.  # noqa: E501

    The version of the OpenAPI document: 1.0.0
    Contact: support@qase.io
    Generated by: https://openapi-generator.tech
"""


import re  # noqa: F401
import sys  # noqa: F401

from qaseio.api_client import ApiClient, Endpoint as _Endpoint
from qaseio.model_utils import (  # noqa: F401
    check_allowed_values,
    check_validations,
    date,
    datetime,
    file_type,
    none_type,
    validate_and_convert_types
)
from qaseio.model.project_access import ProjectAccess
from qaseio.model.project_code_response import ProjectCodeResponse
from qaseio.model.project_create import ProjectCreate
from qaseio.model.project_list_response import ProjectListResponse
from qaseio.model.project_response import ProjectResponse
from qaseio.model.response import Response


class ProjectsApi(object):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client
        self.create_project_endpoint = _Endpoint(
            settings={
                'response_type': (ProjectCodeResponse,),
                'auth': [
                    'TokenAuth'
                ],
                'endpoint_path': '/project',
                'operation_id': 'create_project',
                'http_method': 'POST',
                'servers': None,
            },
            params_map={
                'all': [
                    'project_create',
                ],
                'required': [
                    'project_create',
                ],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                ]
            },
            root_map={
                'validations': {
                },
                'allowed_values': {
                },
                'openapi_types': {
                    'project_create':
                        (ProjectCreate,),
                },
                'attribute_map': {
                },
                'location_map': {
                    'project_create': 'body',
                },
                'collection_format_map': {
                }
            },
            headers_map={
                'accept': [
                    'application/json'
                ],
                'content_type': [
                    'application/json'
                ]
            },
            api_client=api_client
        )
        self.delete_project_endpoint = _Endpoint(
            settings={
                'response_type': (Response,),
                'auth': [
                    'TokenAuth'
                ],
                'endpoint_path': '/project/{code}',
                'operation_id': 'delete_project',
                'http_method': 'DELETE',
                'servers': None,
            },
            params_map={
                'all': [
                    'code',
                ],
                'required': [
                    'code',
                ],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                    'code',
                ]
            },
            root_map={
                'validations': {
                    ('code',): {
                        'max_length': 10,
                        'min_length': 2,
                    },
                },
                'allowed_values': {
                },
                'openapi_types': {
                    'code':
                        (str,),
                },
                'attribute_map': {
                    'code': 'code',
                },
                'location_map': {
                    'code': 'path',
                },
                'collection_format_map': {
                }
            },
            headers_map={
                'accept': [
                    'application/json'
                ],
                'content_type': [],
            },
            api_client=api_client
        )
        self.get_project_endpoint = _Endpoint(
            settings={
                'response_type': (ProjectResponse,),
                'auth': [
                    'TokenAuth'
                ],
                'endpoint_path': '/project/{code}',
                'operation_id': 'get_project',
                'http_method': 'GET',
                'servers': None,
            },
            params_map={
                'all': [
                    'code',
                ],
                'required': [
                    'code',
                ],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                    'code',
                ]
            },
            root_map={
                'validations': {
                    ('code',): {
                        'max_length': 10,
                        'min_length': 2,
                    },
                },
                'allowed_values': {
                },
                'openapi_types': {
                    'code':
                        (str,),
                },
                'attribute_map': {
                    'code': 'code',
                },
                'location_map': {
                    'code': 'path',
                },
                'collection_format_map': {
                }
            },
            headers_map={
                'accept': [
                    'application/json'
                ],
                'content_type': [],
            },
            api_client=api_client
        )
        self.get_projects_endpoint = _Endpoint(
            settings={
                'response_type': (ProjectListResponse,),
                'auth': [
                    'TokenAuth'
                ],
                'endpoint_path': '/project',
                'operation_id': 'get_projects',
                'http_method': 'GET',
                'servers': None,
            },
            params_map={
                'all': [
                    'limit',
                    'offset',
                ],
                'required': [],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                    'limit',
                    'offset',
                ]
            },
            root_map={
                'validations': {
                    ('limit',): {

                        'inclusive_maximum': 100,
                        'inclusive_minimum': 1,
                    },
                    ('offset',): {

                        'inclusive_maximum': 100000,
                        'inclusive_minimum': 0,
                    },
                },
                'allowed_values': {
                },
                'openapi_types': {
                    'limit':
                        (int,),
                    'offset':
                        (int,),
                },
                'attribute_map': {
                    'limit': 'limit',
                    'offset': 'offset',
                },
                'location_map': {
                    'limit': 'query',
                    'offset': 'query',
                },
                'collection_format_map': {
                }
            },
            headers_map={
                'accept': [
                    'application/json'
                ],
                'content_type': [],
            },
            api_client=api_client
        )
        self.grant_access_to_project_endpoint = _Endpoint(
            settings={
                'response_type': (Response,),
                'auth': [
                    'TokenAuth'
                ],
                'endpoint_path': '/project/{code}/access',
                'operation_id': 'grant_access_to_project',
                'http_method': 'POST',
                'servers': None,
            },
            params_map={
                'all': [
                    'code',
                    'project_access',
                ],
                'required': [
                    'code',
                    'project_access',
                ],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                    'code',
                ]
            },
            root_map={
                'validations': {
                    ('code',): {
                        'max_length': 10,
                        'min_length': 2,
                    },
                },
                'allowed_values': {
                },
                'openapi_types': {
                    'code':
                        (str,),
                    'project_access':
                        (ProjectAccess,),
                },
                'attribute_map': {
                    'code': 'code',
                },
                'location_map': {
                    'code': 'path',
                    'project_access': 'body',
                },
                'collection_format_map': {
                }
            },
            headers_map={
                'accept': [
                    'application/json'
                ],
                'content_type': [
                    'application/json'
                ]
            },
            api_client=api_client
        )
        self.revoke_access_to_project_endpoint = _Endpoint(
            settings={
                'response_type': (Response,),
                'auth': [
                    'TokenAuth'
                ],
                'endpoint_path': '/project/{code}/access',
                'operation_id': 'revoke_access_to_project',
                'http_method': 'DELETE',
                'servers': None,
            },
            params_map={
                'all': [
                    'code',
                    'project_access',
                ],
                'required': [
                    'code',
                    'project_access',
                ],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                    'code',
                ]
            },
            root_map={
                'validations': {
                    ('code',): {
                        'max_length': 10,
                        'min_length': 2,
                    },
                },
                'allowed_values': {
                },
                'openapi_types': {
                    'code':
                        (str,),
                    'project_access':
                        (ProjectAccess,),
                },
                'attribute_map': {
                    'code': 'code',
                },
                'location_map': {
                    'code': 'path',
                    'project_access': 'body',
                },
                'collection_format_map': {
                }
            },
            headers_map={
                'accept': [
                    'application/json'
                ],
                'content_type': [
                    'application/json'
                ]
            },
            api_client=api_client
        )

    def create_project(
        self,
        project_create,
        **kwargs
    ):
        """Create new project.  # noqa: E501

        This method is used to create a new project through API.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.create_project(project_create, async_req=True)
        >>> result = thread.get()

        Args:
            project_create (ProjectCreate):

        Keyword Args:
            _return_http_data_only (bool): response data without head status
                code and headers. Default is True.
            _preload_content (bool): if False, the urllib3.HTTPResponse object
                will be returned without reading/decoding response data.
                Default is True.
            _request_timeout (int/float/tuple): timeout setting for this request. If
                one number provided, it will be total request timeout. It can also
                be a pair (tuple) of (connection, read) timeouts.
                Default is None.
            _check_input_type (bool): specifies if type checking
                should be done one the data sent to the server.
                Default is True.
            _check_return_type (bool): specifies if type checking
                should be done one the data received from the server.
                Default is True.
            _spec_property_naming (bool): True if the variable names in the input data
                are serialized names, as specified in the OpenAPI document.
                False if the variable names in the input data
                are pythonic names, e.g. snake case (default)
            _content_type (str/None): force body content-type.
                Default is None and content-type will be predicted by allowed
                content-types and body.
            _host_index (int/None): specifies the index of the server
                that we want to use.
                Default is read from the configuration.
            async_req (bool): execute request asynchronously

        Returns:
            ProjectCodeResponse
                If the method is called asynchronously, returns the request
                thread.
        """
        kwargs['async_req'] = kwargs.get(
            'async_req', False
        )
        kwargs['_return_http_data_only'] = kwargs.get(
            '_return_http_data_only', True
        )
        kwargs['_preload_content'] = kwargs.get(
            '_preload_content', True
        )
        kwargs['_request_timeout'] = kwargs.get(
            '_request_timeout', None
        )
        kwargs['_check_input_type'] = kwargs.get(
            '_check_input_type', True
        )
        kwargs['_check_return_type'] = kwargs.get(
            '_check_return_type', True
        )
        kwargs['_spec_property_naming'] = kwargs.get(
            '_spec_property_naming', False
        )
        kwargs['_content_type'] = kwargs.get(
            '_content_type')
        kwargs['_host_index'] = kwargs.get('_host_index')
        kwargs['project_create'] = \
            project_create
        return self.create_project_endpoint.call_with_http_info(**kwargs)

    def delete_project(
        self,
        code,
        **kwargs
    ):
        """Delete Project by code.  # noqa: E501

        This method allows to delete a specific project.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.delete_project(code, async_req=True)
        >>> result = thread.get()

        Args:
            code (str): Code of project, where to search entities.

        Keyword Args:
            _return_http_data_only (bool): response data without head status
                code and headers. Default is True.
            _preload_content (bool): if False, the urllib3.HTTPResponse object
                will be returned without reading/decoding response data.
                Default is True.
            _request_timeout (int/float/tuple): timeout setting for this request. If
                one number provided, it will be total request timeout. It can also
                be a pair (tuple) of (connection, read) timeouts.
                Default is None.
            _check_input_type (bool): specifies if type checking
                should be done one the data sent to the server.
                Default is True.
            _check_return_type (bool): specifies if type checking
                should be done one the data received from the server.
                Default is True.
            _spec_property_naming (bool): True if the variable names in the input data
                are serialized names, as specified in the OpenAPI document.
                False if the variable names in the input data
                are pythonic names, e.g. snake case (default)
            _content_type (str/None): force body content-type.
                Default is None and content-type will be predicted by allowed
                content-types and body.
            _host_index (int/None): specifies the index of the server
                that we want to use.
                Default is read from the configuration.
            async_req (bool): execute request asynchronously

        Returns:
            Response
                If the method is called asynchronously, returns the request
                thread.
        """
        kwargs['async_req'] = kwargs.get(
            'async_req', False
        )
        kwargs['_return_http_data_only'] = kwargs.get(
            '_return_http_data_only', True
        )
        kwargs['_preload_content'] = kwargs.get(
            '_preload_content', True
        )
        kwargs['_request_timeout'] = kwargs.get(
            '_request_timeout', None
        )
        kwargs['_check_input_type'] = kwargs.get(
            '_check_input_type', True
        )
        kwargs['_check_return_type'] = kwargs.get(
            '_check_return_type', True
        )
        kwargs['_spec_property_naming'] = kwargs.get(
            '_spec_property_naming', False
        )
        kwargs['_content_type'] = kwargs.get(
            '_content_type')
        kwargs['_host_index'] = kwargs.get('_host_index')
        kwargs['code'] = \
            code
        return self.delete_project_endpoint.call_with_http_info(**kwargs)

    def get_project(
        self,
        code,
        **kwargs
    ):
        """Get Project by code.  # noqa: E501

        This method allows to retrieve a specific project.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_project(code, async_req=True)
        >>> result = thread.get()

        Args:
            code (str): Code of project, where to search entities.

        Keyword Args:
            _return_http_data_only (bool): response data without head status
                code and headers. Default is True.
            _preload_content (bool): if False, the urllib3.HTTPResponse object
                will be returned without reading/decoding response data.
                Default is True.
            _request_timeout (int/float/tuple): timeout setting for this request. If
                one number provided, it will be total request timeout. It can also
                be a pair (tuple) of (connection, read) timeouts.
                Default is None.
            _check_input_type (bool): specifies if type checking
                should be done one the data sent to the server.
                Default is True.
            _check_return_type (bool): specifies if type checking
                should be done one the data received from the server.
                Default is True.
            _spec_property_naming (bool): True if the variable names in the input data
                are serialized names, as specified in the OpenAPI document.
                False if the variable names in the input data
                are pythonic names, e.g. snake case (default)
            _content_type (str/None): force body content-type.
                Default is None and content-type will be predicted by allowed
                content-types and body.
            _host_index (int/None): specifies the index of the server
                that we want to use.
                Default is read from the configuration.
            async_req (bool): execute request asynchronously

        Returns:
            ProjectResponse
                If the method is called asynchronously, returns the request
                thread.
        """
        kwargs['async_req'] = kwargs.get(
            'async_req', False
        )
        kwargs['_return_http_data_only'] = kwargs.get(
            '_return_http_data_only', True
        )
        kwargs['_preload_content'] = kwargs.get(
            '_preload_content', True
        )
        kwargs['_request_timeout'] = kwargs.get(
            '_request_timeout', None
        )
        kwargs['_check_input_type'] = kwargs.get(
            '_check_input_type', True
        )
        kwargs['_check_return_type'] = kwargs.get(
            '_check_return_type', True
        )
        kwargs['_spec_property_naming'] = kwargs.get(
            '_spec_property_naming', False
        )
        kwargs['_content_type'] = kwargs.get(
            '_content_type')
        kwargs['_host_index'] = kwargs.get('_host_index')
        kwargs['code'] = \
            code
        return self.get_project_endpoint.call_with_http_info(**kwargs)

    def get_projects(
        self,
        **kwargs
    ):
        """Get All Projects.  # noqa: E501

        This method allows to retrieve all projects available for your account. You can limit and offset params to paginate.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_projects(async_req=True)
        >>> result = thread.get()


        Keyword Args:
            limit (int): A number of entities in result set.. [optional] if omitted the server will use the default value of 10
            offset (int): How many entities should be skipped.. [optional] if omitted the server will use the default value of 0
            _return_http_data_only (bool): response data without head status
                code and headers. Default is True.
            _preload_content (bool): if False, the urllib3.HTTPResponse object
                will be returned without reading/decoding response data.
                Default is True.
            _request_timeout (int/float/tuple): timeout setting for this request. If
                one number provided, it will be total request timeout. It can also
                be a pair (tuple) of (connection, read) timeouts.
                Default is None.
            _check_input_type (bool): specifies if type checking
                should be done one the data sent to the server.
                Default is True.
            _check_return_type (bool): specifies if type checking
                should be done one the data received from the server.
                Default is True.
            _spec_property_naming (bool): True if the variable names in the input data
                are serialized names, as specified in the OpenAPI document.
                False if the variable names in the input data
                are pythonic names, e.g. snake case (default)
            _content_type (str/None): force body content-type.
                Default is None and content-type will be predicted by allowed
                content-types and body.
            _host_index (int/None): specifies the index of the server
                that we want to use.
                Default is read from the configuration.
            async_req (bool): execute request asynchronously

        Returns:
            ProjectListResponse
                If the method is called asynchronously, returns the request
                thread.
        """
        kwargs['async_req'] = kwargs.get(
            'async_req', False
        )
        kwargs['_return_http_data_only'] = kwargs.get(
            '_return_http_data_only', True
        )
        kwargs['_preload_content'] = kwargs.get(
            '_preload_content', True
        )
        kwargs['_request_timeout'] = kwargs.get(
            '_request_timeout', None
        )
        kwargs['_check_input_type'] = kwargs.get(
            '_check_input_type', True
        )
        kwargs['_check_return_type'] = kwargs.get(
            '_check_return_type', True
        )
        kwargs['_spec_property_naming'] = kwargs.get(
            '_spec_property_naming', False
        )
        kwargs['_content_type'] = kwargs.get(
            '_content_type')
        kwargs['_host_index'] = kwargs.get('_host_index')
        return self.get_projects_endpoint.call_with_http_info(**kwargs)

    def grant_access_to_project(
        self,
        code,
        project_access,
        **kwargs
    ):
        """Grant access to project by code.  # noqa: E501

        This method allows to grant access to a specific project.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.grant_access_to_project(code, project_access, async_req=True)
        >>> result = thread.get()

        Args:
            code (str): Code of project, where to search entities.
            project_access (ProjectAccess):

        Keyword Args:
            _return_http_data_only (bool): response data without head status
                code and headers. Default is True.
            _preload_content (bool): if False, the urllib3.HTTPResponse object
                will be returned without reading/decoding response data.
                Default is True.
            _request_timeout (int/float/tuple): timeout setting for this request. If
                one number provided, it will be total request timeout. It can also
                be a pair (tuple) of (connection, read) timeouts.
                Default is None.
            _check_input_type (bool): specifies if type checking
                should be done one the data sent to the server.
                Default is True.
            _check_return_type (bool): specifies if type checking
                should be done one the data received from the server.
                Default is True.
            _spec_property_naming (bool): True if the variable names in the input data
                are serialized names, as specified in the OpenAPI document.
                False if the variable names in the input data
                are pythonic names, e.g. snake case (default)
            _content_type (str/None): force body content-type.
                Default is None and content-type will be predicted by allowed
                content-types and body.
            _host_index (int/None): specifies the index of the server
                that we want to use.
                Default is read from the configuration.
            async_req (bool): execute request asynchronously

        Returns:
            Response
                If the method is called asynchronously, returns the request
                thread.
        """
        kwargs['async_req'] = kwargs.get(
            'async_req', False
        )
        kwargs['_return_http_data_only'] = kwargs.get(
            '_return_http_data_only', True
        )
        kwargs['_preload_content'] = kwargs.get(
            '_preload_content', True
        )
        kwargs['_request_timeout'] = kwargs.get(
            '_request_timeout', None
        )
        kwargs['_check_input_type'] = kwargs.get(
            '_check_input_type', True
        )
        kwargs['_check_return_type'] = kwargs.get(
            '_check_return_type', True
        )
        kwargs['_spec_property_naming'] = kwargs.get(
            '_spec_property_naming', False
        )
        kwargs['_content_type'] = kwargs.get(
            '_content_type')
        kwargs['_host_index'] = kwargs.get('_host_index')
        kwargs['code'] = \
            code
        kwargs['project_access'] = \
            project_access
        return self.grant_access_to_project_endpoint.call_with_http_info(**kwargs)

    def revoke_access_to_project(
        self,
        code,
        project_access,
        **kwargs
    ):
        """Revoke access to project by code.  # noqa: E501

        This method allows to revoke access to a specific project.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.revoke_access_to_project(code, project_access, async_req=True)
        >>> result = thread.get()

        Args:
            code (str): Code of project, where to search entities.
            project_access (ProjectAccess):

        Keyword Args:
            _return_http_data_only (bool): response data without head status
                code and headers. Default is True.
            _preload_content (bool): if False, the urllib3.HTTPResponse object
                will be returned without reading/decoding response data.
                Default is True.
            _request_timeout (int/float/tuple): timeout setting for this request. If
                one number provided, it will be total request timeout. It can also
                be a pair (tuple) of (connection, read) timeouts.
                Default is None.
            _check_input_type (bool): specifies if type checking
                should be done one the data sent to the server.
                Default is True.
            _check_return_type (bool): specifies if type checking
                should be done one the data received from the server.
                Default is True.
            _spec_property_naming (bool): True if the variable names in the input data
                are serialized names, as specified in the OpenAPI document.
                False if the variable names in the input data
                are pythonic names, e.g. snake case (default)
            _content_type (str/None): force body content-type.
                Default is None and content-type will be predicted by allowed
                content-types and body.
            _host_index (int/None): specifies the index of the server
                that we want to use.
                Default is read from the configuration.
            async_req (bool): execute request asynchronously

        Returns:
            Response
                If the method is called asynchronously, returns the request
                thread.
        """
        kwargs['async_req'] = kwargs.get(
            'async_req', False
        )
        kwargs['_return_http_data_only'] = kwargs.get(
            '_return_http_data_only', True
        )
        kwargs['_preload_content'] = kwargs.get(
            '_preload_content', True
        )
        kwargs['_request_timeout'] = kwargs.get(
            '_request_timeout', None
        )
        kwargs['_check_input_type'] = kwargs.get(
            '_check_input_type', True
        )
        kwargs['_check_return_type'] = kwargs.get(
            '_check_return_type', True
        )
        kwargs['_spec_property_naming'] = kwargs.get(
            '_spec_property_naming', False
        )
        kwargs['_content_type'] = kwargs.get(
            '_content_type')
        kwargs['_host_index'] = kwargs.get('_host_index')
        kwargs['code'] = \
            code
        kwargs['project_access'] = \
            project_access
        return self.revoke_access_to_project_endpoint.call_with_http_info(**kwargs)

