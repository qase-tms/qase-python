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
import qaseio
from qaseio.api import shared_steps_api
from qaseio.model.shared_step_create import SharedStepCreate
from qaseio.model.hash_response import HashResponse
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
    api_instance = shared_steps_api.SharedStepsApi(api_client)
    code = "code_example" # str | Code of project, where to search entities.
    shared_step_create = SharedStepCreate(
        title="title_example",
        action="action_example",
        expected_result="expected_result_example",
        data="data_example",
        steps=[
            SharedStepContentCreate(
                hash="hash_example",
                action="action_example",
                expected_result="expected_result_example",
                data="data_example",
                attachments=AttachmentHashList([
                    "attachments_example",
                ]),
            ),
        ],
    ) # SharedStepCreate | 

    # example passing only required values which don't have defaults set
    try:
        # Create a new shared step.
        api_response = api_instance.create_shared_step(code, shared_step_create)
        pprint(api_response)
    except qaseio.ApiException as e:
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
import qaseio
from qaseio.api import shared_steps_api
from qaseio.model.hash_response import HashResponse
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
    api_instance = shared_steps_api.SharedStepsApi(api_client)
    code = "code_example" # str | Code of project, where to search entities.
    hash = "hash_example" # str | Hash.

    # example passing only required values which don't have defaults set
    try:
        # Delete shared step.
        api_response = api_instance.delete_shared_step(code, hash)
        pprint(api_response)
    except qaseio.ApiException as e:
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
import qaseio
from qaseio.api import shared_steps_api
from qaseio.model.shared_step_response import SharedStepResponse
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
    api_instance = shared_steps_api.SharedStepsApi(api_client)
    code = "code_example" # str | Code of project, where to search entities.
    hash = "hash_example" # str | Hash.

    # example passing only required values which don't have defaults set
    try:
        # Get a specific shared step.
        api_response = api_instance.get_shared_step(code, hash)
        pprint(api_response)
    except qaseio.ApiException as e:
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
> SharedStepListResponse get_shared_steps(code)

Get all shared steps.

This method allows to retrieve all shared steps stored in selected project. 

### Example

* Api Key Authentication (TokenAuth):

```python
import time
import qaseio
from qaseio.api import shared_steps_api
from qaseio.model.shared_step_list_response import SharedStepListResponse
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
    api_instance = shared_steps_api.SharedStepsApi(api_client)
    code = "code_example" # str | Code of project, where to search entities.
    search = "search_example" # str | Provide a string that will be used to search by name. (optional)
    limit = 10 # int | A number of entities in result set. (optional) if omitted the server will use the default value of 10
    offset = 0 # int | How many entities should be skipped. (optional) if omitted the server will use the default value of 0

    # example passing only required values which don't have defaults set
    try:
        # Get all shared steps.
        api_response = api_instance.get_shared_steps(code)
        pprint(api_response)
    except qaseio.ApiException as e:
        print("Exception when calling SharedStepsApi->get_shared_steps: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get all shared steps.
        api_response = api_instance.get_shared_steps(code, search=search, limit=limit, offset=offset)
        pprint(api_response)
    except qaseio.ApiException as e:
        print("Exception when calling SharedStepsApi->get_shared_steps: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **code** | **str**| Code of project, where to search entities. |
 **search** | **str**| Provide a string that will be used to search by name. | [optional]
 **limit** | **int**| A number of entities in result set. | [optional] if omitted the server will use the default value of 10
 **offset** | **int**| How many entities should be skipped. | [optional] if omitted the server will use the default value of 0

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
import qaseio
from qaseio.api import shared_steps_api
from qaseio.model.shared_step_update import SharedStepUpdate
from qaseio.model.hash_response import HashResponse
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
    api_instance = shared_steps_api.SharedStepsApi(api_client)
    code = "code_example" # str | Code of project, where to search entities.
    hash = "hash_example" # str | Hash.
    shared_step_update = SharedStepUpdate(
        title="title_example",
        action="action_example",
        expected_result="expected_result_example",
        data="data_example",
        steps=[
            SharedStepContentCreate(
                hash="hash_example",
                action="action_example",
                expected_result="expected_result_example",
                data="data_example",
                attachments=AttachmentHashList([
                    "attachments_example",
                ]),
            ),
        ],
    ) # SharedStepUpdate | 

    # example passing only required values which don't have defaults set
    try:
        # Update shared step.
        api_response = api_instance.update_shared_step(code, hash, shared_step_update)
        pprint(api_response)
    except qaseio.ApiException as e:
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

