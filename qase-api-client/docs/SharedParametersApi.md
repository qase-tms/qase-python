# qase.api_client_v1.SharedParametersApi

All URIs are relative to *https://api.qase.io/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_shared_parameter**](SharedParametersApi.md#create_shared_parameter) | **POST** /shared_parameter | Create a new shared parameter
[**delete_shared_parameter**](SharedParametersApi.md#delete_shared_parameter) | **DELETE** /shared_parameter/{id} | Delete shared parameter
[**get_shared_parameter**](SharedParametersApi.md#get_shared_parameter) | **GET** /shared_parameter/{id} | Get a specific shared parameter
[**get_shared_parameters**](SharedParametersApi.md#get_shared_parameters) | **GET** /shared_parameter | Get all shared parameters
[**update_shared_parameter**](SharedParametersApi.md#update_shared_parameter) | **PATCH** /shared_parameter/{id} | Update shared parameter


# **create_shared_parameter**
> UuidResponse create_shared_parameter(shared_parameter_create)

Create a new shared parameter

### Example

* Api Key Authentication (TokenAuth):

```python
import qase.api_client_v1
from qase.api_client_v1.models.shared_parameter_create import SharedParameterCreate
from qase.api_client_v1.models.uuid_response import UuidResponse
from qase.api_client_v1.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://api.qase.io/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = qase.api_client_v1.Configuration(
    host = "https://api.qase.io/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: TokenAuth
configuration.api_key['TokenAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['TokenAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with qase.api_client_v1.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = qase.api_client_v1.SharedParametersApi(api_client)
    shared_parameter_create = qase.api_client_v1.SharedParameterCreate() # SharedParameterCreate | 

    try:
        # Create a new shared parameter
        api_response = api_instance.create_shared_parameter(shared_parameter_create)
        print("The response of SharedParametersApi->create_shared_parameter:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SharedParametersApi->create_shared_parameter: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **shared_parameter_create** | [**SharedParameterCreate**](SharedParameterCreate.md)|  | 

### Return type

[**UuidResponse**](UuidResponse.md)

### Authorization

[TokenAuth](../README.md#TokenAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A shared parameter. |  -  |
**400** | Bad Request. |  -  |
**401** | Unauthorized. |  -  |
**403** | Forbidden. |  -  |
**404** | Not Found. |  -  |
**422** | Unprocessable Entity. |  -  |
**429** | Too Many Requests. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_shared_parameter**
> UuidResponse delete_shared_parameter(id)

Delete shared parameter

Delete shared parameter along with all its usages in test cases and reviews.

### Example

* Api Key Authentication (TokenAuth):

```python
import qase.api_client_v1
from qase.api_client_v1.models.uuid_response import UuidResponse
from qase.api_client_v1.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://api.qase.io/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = qase.api_client_v1.Configuration(
    host = "https://api.qase.io/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: TokenAuth
configuration.api_key['TokenAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['TokenAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with qase.api_client_v1.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = qase.api_client_v1.SharedParametersApi(api_client)
    id = 'id_example' # str | Identifier.

    try:
        # Delete shared parameter
        api_response = api_instance.delete_shared_parameter(id)
        print("The response of SharedParametersApi->delete_shared_parameter:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SharedParametersApi->delete_shared_parameter: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Identifier. | 

### Return type

[**UuidResponse**](UuidResponse.md)

### Authorization

[TokenAuth](../README.md#TokenAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success. |  -  |
**400** | Bad Request. |  -  |
**401** | Unauthorized. |  -  |
**403** | Forbidden. |  -  |
**404** | Not Found. |  -  |
**429** | Too Many Requests. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_shared_parameter**
> SharedParameterResponse get_shared_parameter(id)

Get a specific shared parameter

### Example

* Api Key Authentication (TokenAuth):

```python
import qase.api_client_v1
from qase.api_client_v1.models.shared_parameter_response import SharedParameterResponse
from qase.api_client_v1.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://api.qase.io/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = qase.api_client_v1.Configuration(
    host = "https://api.qase.io/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: TokenAuth
configuration.api_key['TokenAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['TokenAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with qase.api_client_v1.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = qase.api_client_v1.SharedParametersApi(api_client)
    id = 'id_example' # str | Identifier.

    try:
        # Get a specific shared parameter
        api_response = api_instance.get_shared_parameter(id)
        print("The response of SharedParametersApi->get_shared_parameter:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SharedParametersApi->get_shared_parameter: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Identifier. | 

### Return type

[**SharedParameterResponse**](SharedParameterResponse.md)

### Authorization

[TokenAuth](../README.md#TokenAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A shared parameter. |  -  |
**400** | Bad Request. |  -  |
**401** | Unauthorized. |  -  |
**403** | Forbidden. |  -  |
**404** | Not Found. |  -  |
**429** | Too Many Requests. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_shared_parameters**
> SharedParameterListResponse get_shared_parameters(limit=limit, offset=offset, filters_search=filters_search, filters_type=filters_type, filters_project_codes=filters_project_codes)

Get all shared parameters

### Example

* Api Key Authentication (TokenAuth):

```python
import qase.api_client_v1
from qase.api_client_v1.models.shared_parameter_list_response import SharedParameterListResponse
from qase.api_client_v1.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://api.qase.io/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = qase.api_client_v1.Configuration(
    host = "https://api.qase.io/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: TokenAuth
configuration.api_key['TokenAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['TokenAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with qase.api_client_v1.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = qase.api_client_v1.SharedParametersApi(api_client)
    limit = 10 # int | A number of entities in result set. (optional) (default to 10)
    offset = 0 # int | How many entities should be skipped. (optional) (default to 0)
    filters_search = 'filters_search_example' # str |  (optional)
    filters_type = 'filters_type_example' # str |  (optional)
    filters_project_codes = ['filters_project_codes_example'] # List[str] |  (optional)

    try:
        # Get all shared parameters
        api_response = api_instance.get_shared_parameters(limit=limit, offset=offset, filters_search=filters_search, filters_type=filters_type, filters_project_codes=filters_project_codes)
        print("The response of SharedParametersApi->get_shared_parameters:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SharedParametersApi->get_shared_parameters: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **int**| A number of entities in result set. | [optional] [default to 10]
 **offset** | **int**| How many entities should be skipped. | [optional] [default to 0]
 **filters_search** | **str**|  | [optional] 
 **filters_type** | **str**|  | [optional] 
 **filters_project_codes** | [**List[str]**](str.md)|  | [optional] 

### Return type

[**SharedParameterListResponse**](SharedParameterListResponse.md)

### Authorization

[TokenAuth](../README.md#TokenAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A list of all shared parameters. |  -  |
**400** | Bad Request. |  -  |
**401** | Unauthorized. |  -  |
**403** | Forbidden. |  -  |
**404** | Not Found. |  -  |
**429** | Too Many Requests. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_shared_parameter**
> UuidResponse update_shared_parameter(id, shared_parameter_update)

Update shared parameter

### Example

* Api Key Authentication (TokenAuth):

```python
import qase.api_client_v1
from qase.api_client_v1.models.shared_parameter_update import SharedParameterUpdate
from qase.api_client_v1.models.uuid_response import UuidResponse
from qase.api_client_v1.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://api.qase.io/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = qase.api_client_v1.Configuration(
    host = "https://api.qase.io/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: TokenAuth
configuration.api_key['TokenAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['TokenAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with qase.api_client_v1.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = qase.api_client_v1.SharedParametersApi(api_client)
    id = 'id_example' # str | Identifier.
    shared_parameter_update = qase.api_client_v1.SharedParameterUpdate() # SharedParameterUpdate | 

    try:
        # Update shared parameter
        api_response = api_instance.update_shared_parameter(id, shared_parameter_update)
        print("The response of SharedParametersApi->update_shared_parameter:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SharedParametersApi->update_shared_parameter: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Identifier. | 
 **shared_parameter_update** | [**SharedParameterUpdate**](SharedParameterUpdate.md)|  | 

### Return type

[**UuidResponse**](UuidResponse.md)

### Authorization

[TokenAuth](../README.md#TokenAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK. |  -  |
**400** | Bad Request. |  -  |
**401** | Unauthorized. |  -  |
**403** | Forbidden. |  -  |
**404** | Not Found. |  -  |
**429** | Too Many Requests. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

