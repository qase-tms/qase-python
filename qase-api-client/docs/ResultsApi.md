# qase.api_client_v1.ResultsApi

All URIs are relative to *https://api.qase.io/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_result**](ResultsApi.md#create_result) | **POST** /result/{code}/{id} | Create test run result
[**create_result_bulk**](ResultsApi.md#create_result_bulk) | **POST** /result/{code}/{id}/bulk | Bulk create test run result
[**delete_result**](ResultsApi.md#delete_result) | **DELETE** /result/{code}/{id}/{hash} | Delete test run result
[**get_result**](ResultsApi.md#get_result) | **GET** /result/{code}/{hash} | Get test run result by code
[**get_results**](ResultsApi.md#get_results) | **GET** /result/{code} | Get all test run results
[**update_result**](ResultsApi.md#update_result) | **PATCH** /result/{code}/{id}/{hash} | Update test run result


# **create_result**
> ResultCreateResponse create_result(code, id, result_create)

Create test run result

This method allows to create test run result by Run Id.


### Example

* Api Key Authentication (TokenAuth):

```python
import qase.api_client_v1
from qase.api_client_v1.models.result_create import ResultCreate
from qase.api_client_v1.models.result_create_response import ResultCreateResponse
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
    api_instance = qase.api_client_v1.ResultsApi(api_client)
    code = 'code_example' # str | Code of project, where to search entities.
    id = 56 # int | Identifier.
    result_create = qase.api_client_v1.ResultCreate() # ResultCreate | 

    try:
        # Create test run result
        api_response = api_instance.create_result(code, id, result_create)
        print("The response of ResultsApi->create_result:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ResultsApi->create_result: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **code** | **str**| Code of project, where to search entities. | 
 **id** | **int**| Identifier. | 
 **result_create** | [**ResultCreate**](ResultCreate.md)|  | 

### Return type

[**ResultCreateResponse**](ResultCreateResponse.md)

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

# **create_result_bulk**
> BaseResponse create_result_bulk(code, id, result_create_bulk)

Bulk create test run result

This method allows to create a lot of test run result at once.

If you try to send more than 2,000 results in a single bulk request, you will receive an error with code 413 - Payload Too Large.

If there is no free space left in your team account, when attempting to upload an attachment, e.g., through reporters, you will receive an error with code 507 - Insufficient Storage.


### Example

* Api Key Authentication (TokenAuth):

```python
import qase.api_client_v1
from qase.api_client_v1.models.base_response import BaseResponse
from qase.api_client_v1.models.result_create_bulk import ResultCreateBulk
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
    api_instance = qase.api_client_v1.ResultsApi(api_client)
    code = 'code_example' # str | Code of project, where to search entities.
    id = 56 # int | Identifier.
    result_create_bulk = qase.api_client_v1.ResultCreateBulk() # ResultCreateBulk | 

    try:
        # Bulk create test run result
        api_response = api_instance.create_result_bulk(code, id, result_create_bulk)
        print("The response of ResultsApi->create_result_bulk:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ResultsApi->create_result_bulk: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **code** | **str**| Code of project, where to search entities. | 
 **id** | **int**| Identifier. | 
 **result_create_bulk** | [**ResultCreateBulk**](ResultCreateBulk.md)|  | 

### Return type

[**BaseResponse**](BaseResponse.md)

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
**413** | Payload Too Large. |  -  |
**422** | Unprocessable Entity. |  -  |
**429** | Too Many Requests. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_result**
> HashResponse delete_result(code, id, hash)

Delete test run result

This method allows to delete test run result.


### Example

* Api Key Authentication (TokenAuth):

```python
import qase.api_client_v1
from qase.api_client_v1.models.hash_response import HashResponse
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
    api_instance = qase.api_client_v1.ResultsApi(api_client)
    code = 'code_example' # str | Code of project, where to search entities.
    id = 56 # int | Identifier.
    hash = 'hash_example' # str | Hash.

    try:
        # Delete test run result
        api_response = api_instance.delete_result(code, id, hash)
        print("The response of ResultsApi->delete_result:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ResultsApi->delete_result: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **code** | **str**| Code of project, where to search entities. | 
 **id** | **int**| Identifier. | 
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
**200** | A result. |  -  |
**400** | Bad Request. |  -  |
**401** | Unauthorized. |  -  |
**403** | Forbidden. |  -  |
**404** | Not Found. |  -  |
**429** | Too Many Requests. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_result**
> ResultResponse get_result(code, hash)

Get test run result by code

This method allows to retrieve a specific test run result by Hash.


### Example

* Api Key Authentication (TokenAuth):

```python
import qase.api_client_v1
from qase.api_client_v1.models.result_response import ResultResponse
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
    api_instance = qase.api_client_v1.ResultsApi(api_client)
    code = 'code_example' # str | Code of project, where to search entities.
    hash = 'hash_example' # str | Hash.

    try:
        # Get test run result by code
        api_response = api_instance.get_result(code, hash)
        print("The response of ResultsApi->get_result:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ResultsApi->get_result: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **code** | **str**| Code of project, where to search entities. | 
 **hash** | **str**| Hash. | 

### Return type

[**ResultResponse**](ResultResponse.md)

### Authorization

[TokenAuth](../README.md#TokenAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A test run result. |  -  |
**400** | Bad Request. |  -  |
**401** | Unauthorized. |  -  |
**403** | Forbidden. |  -  |
**404** | Not Found. |  -  |
**429** | Too Many Requests. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_results**
> ResultListResponse get_results(code, status=status, run=run, case_id=case_id, member=member, api=api, from_end_time=from_end_time, to_end_time=to_end_time, limit=limit, offset=offset)

Get all test run results

This method allows to retrieve all test run
results stored in selected project.


### Example

* Api Key Authentication (TokenAuth):

```python
import qase.api_client_v1
from qase.api_client_v1.models.result_list_response import ResultListResponse
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
    api_instance = qase.api_client_v1.ResultsApi(api_client)
    code = 'code_example' # str | Code of project, where to search entities.
    status = 'status_example' # str | A single test run result status. Possible values: in_progress, passed, failed, blocked, skipped, invalid.  (optional)
    run = 'run_example' # str | A list of run IDs separated by comma. (optional)
    case_id = 'case_id_example' # str | A list of case IDs separated by comma. (optional)
    member = 'member_example' # str | A list of member IDs separated by comma. (optional)
    api = True # bool |  (optional)
    from_end_time = 'from_end_time_example' # str | Will return all results created after provided datetime. Allowed format: `Y-m-d H:i:s`.  (optional)
    to_end_time = 'to_end_time_example' # str | Will return all results created before provided datetime. Allowed format: `Y-m-d H:i:s`.  (optional)
    limit = 10 # int | A number of entities in result set. (optional) (default to 10)
    offset = 0 # int | How many entities should be skipped. (optional) (default to 0)

    try:
        # Get all test run results
        api_response = api_instance.get_results(code, status=status, run=run, case_id=case_id, member=member, api=api, from_end_time=from_end_time, to_end_time=to_end_time, limit=limit, offset=offset)
        print("The response of ResultsApi->get_results:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ResultsApi->get_results: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **code** | **str**| Code of project, where to search entities. | 
 **status** | **str**| A single test run result status. Possible values: in_progress, passed, failed, blocked, skipped, invalid.  | [optional] 
 **run** | **str**| A list of run IDs separated by comma. | [optional] 
 **case_id** | **str**| A list of case IDs separated by comma. | [optional] 
 **member** | **str**| A list of member IDs separated by comma. | [optional] 
 **api** | **bool**|  | [optional] 
 **from_end_time** | **str**| Will return all results created after provided datetime. Allowed format: &#x60;Y-m-d H:i:s&#x60;.  | [optional] 
 **to_end_time** | **str**| Will return all results created before provided datetime. Allowed format: &#x60;Y-m-d H:i:s&#x60;.  | [optional] 
 **limit** | **int**| A number of entities in result set. | [optional] [default to 10]
 **offset** | **int**| How many entities should be skipped. | [optional] [default to 0]

### Return type

[**ResultListResponse**](ResultListResponse.md)

### Authorization

[TokenAuth](../README.md#TokenAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A list of all test run results. |  -  |
**400** | Bad Request. |  -  |
**401** | Unauthorized. |  -  |
**403** | Forbidden. |  -  |
**404** | Not Found. |  -  |
**429** | Too Many Requests. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_result**
> HashResponse update_result(code, id, hash, result_update)

Update test run result

This method allows to update test run result.


### Example

* Api Key Authentication (TokenAuth):

```python
import qase.api_client_v1
from qase.api_client_v1.models.hash_response import HashResponse
from qase.api_client_v1.models.result_update import ResultUpdate
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
    api_instance = qase.api_client_v1.ResultsApi(api_client)
    code = 'code_example' # str | Code of project, where to search entities.
    id = 56 # int | Identifier.
    hash = 'hash_example' # str | Hash.
    result_update = qase.api_client_v1.ResultUpdate() # ResultUpdate | 

    try:
        # Update test run result
        api_response = api_instance.update_result(code, id, hash, result_update)
        print("The response of ResultsApi->update_result:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ResultsApi->update_result: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **code** | **str**| Code of project, where to search entities. | 
 **id** | **int**| Identifier. | 
 **hash** | **str**| Hash. | 
 **result_update** | [**ResultUpdate**](ResultUpdate.md)|  | 

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

