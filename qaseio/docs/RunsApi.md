# qaseio.RunsApi

All URIs are relative to *https://api.qase.io/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**complete_run**](RunsApi.md#complete_run) | **POST** /run/{code}/{id}/complete | Complete a specific run.
[**create_run**](RunsApi.md#create_run) | **POST** /run/{code} | Create a new run.
[**delete_run**](RunsApi.md#delete_run) | **DELETE** /run/{code}/{id} | Delete run.
[**get_run**](RunsApi.md#get_run) | **GET** /run/{code}/{id} | Get a specific run.
[**get_runs**](RunsApi.md#get_runs) | **GET** /run/{code} | Get all runs.
[**update_run_publicity**](RunsApi.md#update_run_publicity) | **PATCH** /run/{code}/{id}/public | Update publicity of a specific run.


# **complete_run**
> Response complete_run(code, id)

Complete a specific run.

This method allows to complete a specific run. 

### Example

* Api Key Authentication (TokenAuth):

```python
import time
import qaseio
from qaseio.api import runs_api
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
    api_instance = runs_api.RunsApi(api_client)
    code = "code_example" # str | Code of project, where to search entities.
    id = 1 # int | Identifier.

    # example passing only required values which don't have defaults set
    try:
        # Complete a specific run.
        api_response = api_instance.complete_run(code, id)
        pprint(api_response)
    except qaseio.ApiException as e:
        print("Exception when calling RunsApi->complete_run: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **code** | **str**| Code of project, where to search entities. |
 **id** | **int**| Identifier. |

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
**200** | A result. |  -  |
**400** | Bad Request. |  -  |
**401** | Unauthorized. |  -  |
**403** | Forbidden. |  -  |
**404** | Not Found. |  -  |
**422** | Unprocessable Entity. |  -  |
**429** | Too Many Requests. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_run**
> IdResponse create_run(code, run_create)

Create a new run.

This method allows to create a run in selected project. 

### Example

* Api Key Authentication (TokenAuth):

```python
import time
import qaseio
from qaseio.api import runs_api
from qaseio.model.run_create import RunCreate
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
    api_instance = runs_api.RunsApi(api_client)
    code = "code_example" # str | Code of project, where to search entities.
    run_create = RunCreate(
        title="title_example",
        description="description_example",
        include_all_cases=True,
        cases=[
            1,
        ],
        is_autotest=True,
        environment_id=1,
        milestone_id=1,
        plan_id=1,
        tags=[
            "tags_example",
        ],
        custom_field={
            "key": "key_example",
        },
        start_time="start_time_example",
        end_time="end_time_example",
    ) # RunCreate | 

    # example passing only required values which don't have defaults set
    try:
        # Create a new run.
        api_response = api_instance.create_run(code, run_create)
        pprint(api_response)
    except qaseio.ApiException as e:
        print("Exception when calling RunsApi->create_run: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **code** | **str**| Code of project, where to search entities. |
 **run_create** | [**RunCreate**](RunCreate.md)|  |

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

# **delete_run**
> IdResponse delete_run(code, id)

Delete run.

This method completely deletes a run from repository. 

### Example

* Api Key Authentication (TokenAuth):

```python
import time
import qaseio
from qaseio.api import runs_api
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
    api_instance = runs_api.RunsApi(api_client)
    code = "code_example" # str | Code of project, where to search entities.
    id = 1 # int | Identifier.

    # example passing only required values which don't have defaults set
    try:
        # Delete run.
        api_response = api_instance.delete_run(code, id)
        pprint(api_response)
    except qaseio.ApiException as e:
        print("Exception when calling RunsApi->delete_run: %s\n" % e)
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

# **get_run**
> RunResponse get_run(code, id)

Get a specific run.

This method allows to retrieve a specific run. 

### Example

* Api Key Authentication (TokenAuth):

```python
import time
import qaseio
from qaseio.api import runs_api
from qaseio.model.run_response import RunResponse
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
    api_instance = runs_api.RunsApi(api_client)
    code = "code_example" # str | Code of project, where to search entities.
    id = 1 # int | Identifier.
    include = "include_example" # str | Include a list of related entities IDs into response. Should be separated by comma. Possible values: cases, defects  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get a specific run.
        api_response = api_instance.get_run(code, id)
        pprint(api_response)
    except qaseio.ApiException as e:
        print("Exception when calling RunsApi->get_run: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get a specific run.
        api_response = api_instance.get_run(code, id, include=include)
        pprint(api_response)
    except qaseio.ApiException as e:
        print("Exception when calling RunsApi->get_run: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **code** | **str**| Code of project, where to search entities. |
 **id** | **int**| Identifier. |
 **include** | **str**| Include a list of related entities IDs into response. Should be separated by comma. Possible values: cases, defects  | [optional]

### Return type

[**RunResponse**](RunResponse.md)

### Authorization

[TokenAuth](../README.md#TokenAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A run. |  -  |
**400** | Bad Request. |  -  |
**401** | Unauthorized. |  -  |
**403** | Forbidden. |  -  |
**404** | Not Found. |  -  |
**429** | Too Many Requests. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_runs**
> RunListResponse get_runs(code)

Get all runs.

This method allows to retrieve all runs stored in selected project. 

### Example

* Api Key Authentication (TokenAuth):

```python
import time
import qaseio
from qaseio.api import runs_api
from qaseio.model.run_list_response import RunListResponse
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
    api_instance = runs_api.RunsApi(api_client)
    code = "code_example" # str | Code of project, where to search entities.
    search = "search_example" # str |  (optional)
    status = "status_example" # str | A list of status values separated by comma. Possible values: active, complete, abort.  (optional)
    milestone = 1 # int |  (optional)
    environment = 1 # int |  (optional)
    from_start_time = 1 # int |  (optional)
    to_start_time = 1 # int |  (optional)
    limit = 10 # int | A number of entities in result set. (optional) if omitted the server will use the default value of 10
    offset = 0 # int | How many entities should be skipped. (optional) if omitted the server will use the default value of 0
    include = "include_example" # str | Include a list of related entities IDs into response. Should be separated by comma. Possible values: cases, defects  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get all runs.
        api_response = api_instance.get_runs(code)
        pprint(api_response)
    except qaseio.ApiException as e:
        print("Exception when calling RunsApi->get_runs: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get all runs.
        api_response = api_instance.get_runs(code, search=search, status=status, milestone=milestone, environment=environment, from_start_time=from_start_time, to_start_time=to_start_time, limit=limit, offset=offset, include=include)
        pprint(api_response)
    except qaseio.ApiException as e:
        print("Exception when calling RunsApi->get_runs: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **code** | **str**| Code of project, where to search entities. |
 **search** | **str**|  | [optional]
 **status** | **str**| A list of status values separated by comma. Possible values: active, complete, abort.  | [optional]
 **milestone** | **int**|  | [optional]
 **environment** | **int**|  | [optional]
 **from_start_time** | **int**|  | [optional]
 **to_start_time** | **int**|  | [optional]
 **limit** | **int**| A number of entities in result set. | [optional] if omitted the server will use the default value of 10
 **offset** | **int**| How many entities should be skipped. | [optional] if omitted the server will use the default value of 0
 **include** | **str**| Include a list of related entities IDs into response. Should be separated by comma. Possible values: cases, defects  | [optional]

### Return type

[**RunListResponse**](RunListResponse.md)

### Authorization

[TokenAuth](../README.md#TokenAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A list of all runs. |  -  |
**400** | Bad Request. |  -  |
**401** | Unauthorized. |  -  |
**403** | Forbidden. |  -  |
**404** | Not Found. |  -  |
**429** | Too Many Requests. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_run_publicity**
> RunPublicResponse update_run_publicity(code, id, run_public)

Update publicity of a specific run.

This method allows to update a publicity of specific run. 

### Example

* Api Key Authentication (TokenAuth):

```python
import time
import qaseio
from qaseio.api import runs_api
from qaseio.model.run_public import RunPublic
from qaseio.model.run_public_response import RunPublicResponse
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
    api_instance = runs_api.RunsApi(api_client)
    code = "code_example" # str | Code of project, where to search entities.
    id = 1 # int | Identifier.
    run_public = RunPublic(
        status=True,
    ) # RunPublic | 

    # example passing only required values which don't have defaults set
    try:
        # Update publicity of a specific run.
        api_response = api_instance.update_run_publicity(code, id, run_public)
        pprint(api_response)
    except qaseio.ApiException as e:
        print("Exception when calling RunsApi->update_run_publicity: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **code** | **str**| Code of project, where to search entities. |
 **id** | **int**| Identifier. |
 **run_public** | [**RunPublic**](RunPublic.md)|  |

### Return type

[**RunPublicResponse**](RunPublicResponse.md)

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

