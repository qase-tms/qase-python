# qaseio.SharedStepsApi

All URIs are relative to *https://api.qase.io/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_shared_step**](SharedStepsApi.md#create_shared_step) | **POST** /shared_step/{code} | Create a new shared step.
[**delete_shared_step**](SharedStepsApi.md#delete_shared_step) | **DELETE** /shared_step/{code}/{hash} | Delete shared step.
[**get_shared_step**](SharedStepsApi.md#get_shared_step) | **GET** /shared_step/{code}/{hash} | Get a specific shared step.
[**get_shared_steps**](SharedStepsApi.md#get_shared_steps) | **GET** /shared_step/{code} | Get all shared steps.
[**update_shared_step**](SharedStepsApi.md#update_shared_step) | **PATCH** /shared_step/{code}/{hash} | Update shared step.


# **create_shared_step**
> HashResponse create_shared_step(code, shared_step_create)

Create a new shared step.

This method allows to create a shared step in selected project. 

### Example

* Api Key Authentication (TokenAuth):

```python
import time
import os
import qaseio
from qaseio.models.hash_response import HashResponse
from qaseio.models.shared_step_create import SharedStepCreate
from qaseio.rest import ApiException
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
configuration.api_key['TokenAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['TokenAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with qaseio.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = qaseio.SharedStepsApi(api_client)
    code = 'code_example' # str | Code of project, where to search entities.
    shared_step_create = qaseio.SharedStepCreate() # SharedStepCreate | 

    try:
        # Create a new shared step.
        api_response = api_instance.create_shared_step(code, shared_step_create)
        print("The response of SharedStepsApi->create_shared_step:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SharedStepsApi->create_shared_step: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **code** | **str**| Code of project, where to search entities. | 
 **shared_step_create** | [**SharedStepCreate**](SharedStepCreate.md)|  | 

### Return type

[**HashResponse**](HashResponse.md)

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

# **delete_shared_step**
> HashResponse delete_shared_step(code, hash)

Delete shared step.

This method completely deletes a shared step from repository. 

### Example

* Api Key Authentication (TokenAuth):

```python
import time
import os
import qaseio
from qaseio.models.hash_response import HashResponse
from qaseio.rest import ApiException
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
configuration.api_key['TokenAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['TokenAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with qaseio.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = qaseio.SharedStepsApi(api_client)
    code = 'code_example' # str | Code of project, where to search entities.
    hash = 'hash_example' # str | Hash.

    try:
        # Delete shared step.
        api_response = api_instance.delete_shared_step(code, hash)
        print("The response of SharedStepsApi->delete_shared_step:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SharedStepsApi->delete_shared_step: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **code** | **str**| Code of project, where to search entities. | 
 **hash** | **str**| Hash. | 

### Return type

[**HashResponse**](HashResponse.md)

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

# **get_shared_step**
> SharedStepResponse get_shared_step(code, hash)

Get a specific shared step.

This method allows to retrieve a specific shared step. 

### Example

* Api Key Authentication (TokenAuth):

```python
import time
import os
import qaseio
from qaseio.models.shared_step_response import SharedStepResponse
from qaseio.rest import ApiException
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
configuration.api_key['TokenAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['TokenAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with qaseio.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = qaseio.SharedStepsApi(api_client)
    code = 'code_example' # str | Code of project, where to search entities.
    hash = 'hash_example' # str | Hash.

    try:
        # Get a specific shared step.
        api_response = api_instance.get_shared_step(code, hash)
        print("The response of SharedStepsApi->get_shared_step:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SharedStepsApi->get_shared_step: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **code** | **str**| Code of project, where to search entities. | 
 **hash** | **str**| Hash. | 

### Return type

[**SharedStepResponse**](SharedStepResponse.md)

### Authorization

[TokenAuth](../README.md#TokenAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A shared step. |  -  |
**400** | Bad Request. |  -  |
**401** | Unauthorized. |  -  |
**403** | Forbidden. |  -  |
**404** | Not Found. |  -  |
**429** | Too Many Requests. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_shared_steps**
> SharedStepListResponse get_shared_steps(code, search=search, limit=limit, offset=offset)

Get all shared steps.

This method allows to retrieve all shared steps stored in selected project. 

### Example

* Api Key Authentication (TokenAuth):

```python
import time
import os
import qaseio
from qaseio.models.shared_step_list_response import SharedStepListResponse
from qaseio.rest import ApiException
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
configuration.api_key['TokenAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['TokenAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with qaseio.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = qaseio.SharedStepsApi(api_client)
    code = 'code_example' # str | Code of project, where to search entities.
    search = 'search_example' # str | Provide a string that will be used to search by name. (optional)
    limit = 10 # int | A number of entities in result set. (optional) (default to 10)
    offset = 0 # int | How many entities should be skipped. (optional) (default to 0)

    try:
        # Get all shared steps.
        api_response = api_instance.get_shared_steps(code, search=search, limit=limit, offset=offset)
        print("The response of SharedStepsApi->get_shared_steps:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SharedStepsApi->get_shared_steps: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **code** | **str**| Code of project, where to search entities. | 
 **search** | **str**| Provide a string that will be used to search by name. | [optional] 
 **limit** | **int**| A number of entities in result set. | [optional] [default to 10]
 **offset** | **int**| How many entities should be skipped. | [optional] [default to 0]

### Return type

[**SharedStepListResponse**](SharedStepListResponse.md)

### Authorization

[TokenAuth](../README.md#TokenAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A list of all shared steps. |  -  |
**400** | Bad Request. |  -  |
**401** | Unauthorized. |  -  |
**403** | Forbidden. |  -  |
**404** | Not Found. |  -  |
**429** | Too Many Requests. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_shared_step**
> HashResponse update_shared_step(code, hash, shared_step_update)

Update shared step.

This method updates a shared step. 

### Example

* Api Key Authentication (TokenAuth):

```python
import time
import os
import qaseio
from qaseio.models.hash_response import HashResponse
from qaseio.models.shared_step_update import SharedStepUpdate
from qaseio.rest import ApiException
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
configuration.api_key['TokenAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['TokenAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with qaseio.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = qaseio.SharedStepsApi(api_client)
    code = 'code_example' # str | Code of project, where to search entities.
    hash = 'hash_example' # str | Hash.
    shared_step_update = qaseio.SharedStepUpdate() # SharedStepUpdate | 

    try:
        # Update shared step.
        api_response = api_instance.update_shared_step(code, hash, shared_step_update)
        print("The response of SharedStepsApi->update_shared_step:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SharedStepsApi->update_shared_step: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **code** | **str**| Code of project, where to search entities. | 
 **hash** | **str**| Hash. | 
 **shared_step_update** | [**SharedStepUpdate**](SharedStepUpdate.md)|  | 

### Return type

[**HashResponse**](HashResponse.md)

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

