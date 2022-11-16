# qaseio.EnvironmentsApi

All URIs are relative to *https://api.qase.io/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_environment**](EnvironmentsApi.md#create_environment) | **POST** /environment/{code} | Create a new environment.
[**delete_environment**](EnvironmentsApi.md#delete_environment) | **DELETE** /environment/{code}/{id} | Delete environment.
[**get_environment**](EnvironmentsApi.md#get_environment) | **GET** /environment/{code}/{id} | Get a specific environment.
[**get_environments**](EnvironmentsApi.md#get_environments) | **GET** /environment/{code} | Get all environments.
[**update_environment**](EnvironmentsApi.md#update_environment) | **PATCH** /environment/{code}/{id} | Update environment.


# **create_environment**
> IdResponse create_environment(code, environment_create)

Create a new environment.

This method allows to create an environment in selected project. 

### Example

* Api Key Authentication (TokenAuth):

```python
import time
import qaseio
from qaseio.api import environments_api
from qaseio.model.id_response import IdResponse
from qaseio.model.environment_create import EnvironmentCreate
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
    api_instance = environments_api.EnvironmentsApi(api_client)
    code = "code_example" # str | Code of project, where to search entities.
    environment_create = EnvironmentCreate(
        title="title_example",
        description="description_example",
        slug="slug_example",
        host="host_example",
    ) # EnvironmentCreate | 

    # example passing only required values which don't have defaults set
    try:
        # Create a new environment.
        api_response = api_instance.create_environment(code, environment_create)
        pprint(api_response)
    except qaseio.ApiException as e:
        print("Exception when calling EnvironmentsApi->create_environment: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **code** | **str**| Code of project, where to search entities. |
 **environment_create** | [**EnvironmentCreate**](EnvironmentCreate.md)|  |

### Return type

[**IdResponse**](IdResponse.md)

### Authorization

[TokenAuth](../README.md#TokenAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A result. |  -  |
**400** | Bad Request. |  -  |
**401** | Unauthorized. |  -  |
**403** | Forbidden. |  -  |
**404** | Not Found. |  -  |
**422** | Unprocessable Entity. |  -  |
**429** | Too Many Requests. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_environment**
> IdResponse delete_environment(code, id)

Delete environment.

This method completely deletes an environment from repository. 

### Example

* Api Key Authentication (TokenAuth):

```python
import time
import qaseio
from qaseio.api import environments_api
from qaseio.model.id_response import IdResponse
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
    api_instance = environments_api.EnvironmentsApi(api_client)
    code = "code_example" # str | Code of project, where to search entities.
    id = 1 # int | Identifier.

    # example passing only required values which don't have defaults set
    try:
        # Delete environment.
        api_response = api_instance.delete_environment(code, id)
        pprint(api_response)
    except qaseio.ApiException as e:
        print("Exception when calling EnvironmentsApi->delete_environment: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **code** | **str**| Code of project, where to search entities. |
 **id** | **int**| Identifier. |

### Return type

[**IdResponse**](IdResponse.md)

### Authorization

[TokenAuth](../README.md#TokenAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A Result. |  -  |
**400** | Bad Request. |  -  |
**401** | Unauthorized. |  -  |
**403** | Forbidden. |  -  |
**404** | Not Found. |  -  |
**429** | Too Many Requests. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_environment**
> EnvironmentResponse get_environment(code, id)

Get a specific environment.

This method allows to retrieve a specific environment. 

### Example

* Api Key Authentication (TokenAuth):

```python
import time
import qaseio
from qaseio.api import environments_api
from qaseio.model.environment_response import EnvironmentResponse
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
    api_instance = environments_api.EnvironmentsApi(api_client)
    code = "code_example" # str | Code of project, where to search entities.
    id = 1 # int | Identifier.

    # example passing only required values which don't have defaults set
    try:
        # Get a specific environment.
        api_response = api_instance.get_environment(code, id)
        pprint(api_response)
    except qaseio.ApiException as e:
        print("Exception when calling EnvironmentsApi->get_environment: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **code** | **str**| Code of project, where to search entities. |
 **id** | **int**| Identifier. |

### Return type

[**EnvironmentResponse**](EnvironmentResponse.md)

### Authorization

[TokenAuth](../README.md#TokenAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | An environment. |  -  |
**400** | Bad Request. |  -  |
**401** | Unauthorized. |  -  |
**403** | Forbidden. |  -  |
**404** | Not Found. |  -  |
**429** | Too Many Requests. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_environments**
> EnvironmentListResponse get_environments(code)

Get all environments.

This method allows to retrieve all environments stored in selected project. 

### Example

* Api Key Authentication (TokenAuth):

```python
import time
import qaseio
from qaseio.api import environments_api
from qaseio.model.environment_list_response import EnvironmentListResponse
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
    api_instance = environments_api.EnvironmentsApi(api_client)
    code = "code_example" # str | Code of project, where to search entities.
    limit = 10 # int | A number of entities in result set. (optional) if omitted the server will use the default value of 10
    offset = 0 # int | How many entities should be skipped. (optional) if omitted the server will use the default value of 0

    # example passing only required values which don't have defaults set
    try:
        # Get all environments.
        api_response = api_instance.get_environments(code)
        pprint(api_response)
    except qaseio.ApiException as e:
        print("Exception when calling EnvironmentsApi->get_environments: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get all environments.
        api_response = api_instance.get_environments(code, limit=limit, offset=offset)
        pprint(api_response)
    except qaseio.ApiException as e:
        print("Exception when calling EnvironmentsApi->get_environments: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **code** | **str**| Code of project, where to search entities. |
 **limit** | **int**| A number of entities in result set. | [optional] if omitted the server will use the default value of 10
 **offset** | **int**| How many entities should be skipped. | [optional] if omitted the server will use the default value of 0

### Return type

[**EnvironmentListResponse**](EnvironmentListResponse.md)

### Authorization

[TokenAuth](../README.md#TokenAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A list of all environments. |  -  |
**400** | Bad Request. |  -  |
**401** | Unauthorized. |  -  |
**403** | Forbidden. |  -  |
**404** | Not Found. |  -  |
**429** | Too Many Requests. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_environment**
> IdResponse update_environment(code, id, environment_update)

Update environment.

This method updates an environment. 

### Example

* Api Key Authentication (TokenAuth):

```python
import time
import qaseio
from qaseio.api import environments_api
from qaseio.model.environment_update import EnvironmentUpdate
from qaseio.model.id_response import IdResponse
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
    api_instance = environments_api.EnvironmentsApi(api_client)
    code = "code_example" # str | Code of project, where to search entities.
    id = 1 # int | Identifier.
    environment_update = EnvironmentUpdate(
        title="title_example",
        description="description_example",
        slug="slug_example",
        host="host_example",
    ) # EnvironmentUpdate | 

    # example passing only required values which don't have defaults set
    try:
        # Update environment.
        api_response = api_instance.update_environment(code, id, environment_update)
        pprint(api_response)
    except qaseio.ApiException as e:
        print("Exception when calling EnvironmentsApi->update_environment: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **code** | **str**| Code of project, where to search entities. |
 **id** | **int**| Identifier. |
 **environment_update** | [**EnvironmentUpdate**](EnvironmentUpdate.md)|  |

### Return type

[**IdResponse**](IdResponse.md)

### Authorization

[TokenAuth](../README.md#TokenAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A result. |  -  |
**400** | Bad Request. |  -  |
**401** | Unauthorized. |  -  |
**403** | Forbidden. |  -  |
**404** | Not Found. |  -  |
**429** | Too Many Requests. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

