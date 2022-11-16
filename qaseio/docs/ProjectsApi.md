# qaseio.ProjectsApi

All URIs are relative to *https://api.qase.io/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_project**](ProjectsApi.md#create_project) | **POST** /project | Create new project.
[**delete_project**](ProjectsApi.md#delete_project) | **DELETE** /project/{code} | Delete Project by code.
[**get_project**](ProjectsApi.md#get_project) | **GET** /project/{code} | Get Project by code.
[**get_projects**](ProjectsApi.md#get_projects) | **GET** /project | Get All Projects.
[**grant_access_to_project**](ProjectsApi.md#grant_access_to_project) | **POST** /project/{code}/access | Grant access to project by code.
[**revoke_access_to_project**](ProjectsApi.md#revoke_access_to_project) | **DELETE** /project/{code}/access | Revoke access to project by code.


# **create_project**
> ProjectCodeResponse create_project(project_create)

Create new project.

This method is used to create a new project through API. 

### Example

* Api Key Authentication (TokenAuth):

```python
import time
import qaseio
from qaseio.api import projects_api
from qaseio.model.project_code_response import ProjectCodeResponse
from qaseio.model.project_create import ProjectCreate
from pprint import pprint
# Defining the host is optional and defaults to https://api.qase.io/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = qaseio.Configuration(
    host = "https://api.qase.io/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: TokenAuth
configuration.api_key['TokenAuth'] = 'YOUR_API_KEY'

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['TokenAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with qaseio.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = projects_api.ProjectsApi(api_client)
    project_create = ProjectCreate(
        title="title_example",
        code="EiOTgsw",
        description="description_example",
        access="all",
        group="group_example",
    ) # ProjectCreate | 

    # example passing only required values which don't have defaults set
    try:
        # Create new project.
        api_response = api_instance.create_project(project_create)
        pprint(api_response)
    except qaseio.ApiException as e:
        print("Exception when calling ProjectsApi->create_project: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_create** | [**ProjectCreate**](ProjectCreate.md)|  |

### Return type

[**ProjectCodeResponse**](ProjectCodeResponse.md)

### Authorization

[TokenAuth](../README.md#TokenAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A result of project creation. |  -  |
**400** | Bad Request. |  -  |
**401** | Unauthorized. |  -  |
**403** | Forbidden. |  -  |
**422** | Unprocessable Entity. |  -  |
**429** | Too Many Requests. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_project**
> Response delete_project(code)

Delete Project by code.

This method allows to delete a specific project. 

### Example

* Api Key Authentication (TokenAuth):

```python
import time
import qaseio
from qaseio.api import projects_api
from qaseio.model.response import Response
from pprint import pprint
# Defining the host is optional and defaults to https://api.qase.io/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = qaseio.Configuration(
    host = "https://api.qase.io/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: TokenAuth
configuration.api_key['TokenAuth'] = 'YOUR_API_KEY'

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['TokenAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with qaseio.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = projects_api.ProjectsApi(api_client)
    code = "code_example" # str | Code of project, where to search entities.

    # example passing only required values which don't have defaults set
    try:
        # Delete Project by code.
        api_response = api_instance.delete_project(code)
        pprint(api_response)
    except qaseio.ApiException as e:
        print("Exception when calling ProjectsApi->delete_project: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **code** | **str**| Code of project, where to search entities. |

### Return type

[**Response**](Response.md)

### Authorization

[TokenAuth](../README.md#TokenAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A result of project removal. |  -  |
**400** | Bad Request. |  -  |
**401** | Unauthorized. |  -  |
**403** | Forbidden. |  -  |
**404** | Not Found. |  -  |
**429** | Too Many Requests. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_project**
> ProjectResponse get_project(code)

Get Project by code.

This method allows to retrieve a specific project. 

### Example

* Api Key Authentication (TokenAuth):

```python
import time
import qaseio
from qaseio.api import projects_api
from qaseio.model.project_response import ProjectResponse
from pprint import pprint
# Defining the host is optional and defaults to https://api.qase.io/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = qaseio.Configuration(
    host = "https://api.qase.io/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: TokenAuth
configuration.api_key['TokenAuth'] = 'YOUR_API_KEY'

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['TokenAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with qaseio.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = projects_api.ProjectsApi(api_client)
    code = "code_example" # str | Code of project, where to search entities.

    # example passing only required values which don't have defaults set
    try:
        # Get Project by code.
        api_response = api_instance.get_project(code)
        pprint(api_response)
    except qaseio.ApiException as e:
        print("Exception when calling ProjectsApi->get_project: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **code** | **str**| Code of project, where to search entities. |

### Return type

[**ProjectResponse**](ProjectResponse.md)

### Authorization

[TokenAuth](../README.md#TokenAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A Project. |  -  |
**400** | Bad Request. |  -  |
**401** | Unauthorized. |  -  |
**403** | Forbidden. |  -  |
**404** | Not Found. |  -  |
**429** | Too Many Requests. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_projects**
> ProjectListResponse get_projects()

Get All Projects.

This method allows to retrieve all projects available for your account. You can limit and offset params to paginate. 

### Example

* Api Key Authentication (TokenAuth):

```python
import time
import qaseio
from qaseio.api import projects_api
from qaseio.model.project_list_response import ProjectListResponse
from pprint import pprint
# Defining the host is optional and defaults to https://api.qase.io/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = qaseio.Configuration(
    host = "https://api.qase.io/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: TokenAuth
configuration.api_key['TokenAuth'] = 'YOUR_API_KEY'

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['TokenAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with qaseio.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = projects_api.ProjectsApi(api_client)
    limit = 10 # int | A number of entities in result set. (optional) if omitted the server will use the default value of 10
    offset = 0 # int | How many entities should be skipped. (optional) if omitted the server will use the default value of 0

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get All Projects.
        api_response = api_instance.get_projects(limit=limit, offset=offset)
        pprint(api_response)
    except qaseio.ApiException as e:
        print("Exception when calling ProjectsApi->get_projects: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **int**| A number of entities in result set. | [optional] if omitted the server will use the default value of 10
 **offset** | **int**| How many entities should be skipped. | [optional] if omitted the server will use the default value of 0

### Return type

[**ProjectListResponse**](ProjectListResponse.md)

### Authorization

[TokenAuth](../README.md#TokenAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A list of all projects. |  -  |
**400** | Bad Request. |  -  |
**401** | Unauthorized. |  -  |
**403** | Forbidden. |  -  |
**429** | Too Many Requests. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **grant_access_to_project**
> Response grant_access_to_project(code, project_access)

Grant access to project by code.

This method allows to grant access to a specific project. 

### Example

* Api Key Authentication (TokenAuth):

```python
import time
import qaseio
from qaseio.api import projects_api
from qaseio.model.response import Response
from qaseio.model.project_access import ProjectAccess
from pprint import pprint
# Defining the host is optional and defaults to https://api.qase.io/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = qaseio.Configuration(
    host = "https://api.qase.io/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: TokenAuth
configuration.api_key['TokenAuth'] = 'YOUR_API_KEY'

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['TokenAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with qaseio.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = projects_api.ProjectsApi(api_client)
    code = "code_example" # str | Code of project, where to search entities.
    project_access = ProjectAccess(
        member_id=1,
    ) # ProjectAccess | 

    # example passing only required values which don't have defaults set
    try:
        # Grant access to project by code.
        api_response = api_instance.grant_access_to_project(code, project_access)
        pprint(api_response)
    except qaseio.ApiException as e:
        print("Exception when calling ProjectsApi->grant_access_to_project: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **code** | **str**| Code of project, where to search entities. |
 **project_access** | [**ProjectAccess**](ProjectAccess.md)|  |

### Return type

[**Response**](Response.md)

### Authorization

[TokenAuth](../README.md#TokenAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Result of operation. |  -  |
**400** | Bad Request. |  -  |
**401** | Unauthorized. |  -  |
**403** | Forbidden. |  -  |
**404** | Not Found. |  -  |
**422** | Unprocessable Entity. |  -  |
**429** | Too Many Requests. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **revoke_access_to_project**
> Response revoke_access_to_project(code, project_access)

Revoke access to project by code.

This method allows to revoke access to a specific project. 

### Example

* Api Key Authentication (TokenAuth):

```python
import time
import qaseio
from qaseio.api import projects_api
from qaseio.model.response import Response
from qaseio.model.project_access import ProjectAccess
from pprint import pprint
# Defining the host is optional and defaults to https://api.qase.io/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = qaseio.Configuration(
    host = "https://api.qase.io/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: TokenAuth
configuration.api_key['TokenAuth'] = 'YOUR_API_KEY'

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['TokenAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with qaseio.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = projects_api.ProjectsApi(api_client)
    code = "code_example" # str | Code of project, where to search entities.
    project_access = ProjectAccess(
        member_id=1,
    ) # ProjectAccess | 

    # example passing only required values which don't have defaults set
    try:
        # Revoke access to project by code.
        api_response = api_instance.revoke_access_to_project(code, project_access)
        pprint(api_response)
    except qaseio.ApiException as e:
        print("Exception when calling ProjectsApi->revoke_access_to_project: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **code** | **str**| Code of project, where to search entities. |
 **project_access** | [**ProjectAccess**](ProjectAccess.md)|  |

### Return type

[**Response**](Response.md)

### Authorization

[TokenAuth](../README.md#TokenAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Result of operation. |  -  |
**400** | Bad Request. |  -  |
**401** | Unauthorized. |  -  |
**403** | Forbidden. |  -  |
**404** | Not Found. |  -  |
**422** | Unprocessable Entity. |  -  |
**429** | Too Many Requests. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

