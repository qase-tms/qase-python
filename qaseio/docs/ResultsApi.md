# qaseio.ResultsApi

All URIs are relative to *https://api.qase.io/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_result**](ResultsApi.md#create_result) | **POST** /result/{code}/{id} | Create test run result.
[**create_result_bulk**](ResultsApi.md#create_result_bulk) | **POST** /result/{code}/{id}/bulk | Bulk create test run result.
[**delete_result**](ResultsApi.md#delete_result) | **DELETE** /result/{code}/{id}/{hash} | Delete test run result.
[**get_result**](ResultsApi.md#get_result) | **GET** /result/{code}/{hash} | Get test run result by code.
[**get_results**](ResultsApi.md#get_results) | **GET** /result/{code} | Get all test run results.
[**update_result**](ResultsApi.md#update_result) | **PATCH** /result/{code}/{id}/{hash} | Update test run result.


# **create_result**
> CreateResult200Response create_result(code, id, result_create)

Create test run result.

This method allows to create test run result by Run Id. 

### Example

* Api Key Authentication (TokenAuth):

```python
import time
import qaseio
from qaseio.api import results_api
from qaseio.model.result_create import ResultCreate
from qaseio.model.create_result200_response import CreateResult200Response
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
    api_instance = results_api.ResultsApi(api_client)
    code = "code_example" # str | Code of project, where to search entities.
    id = 1 # int | Identifier.
    result_create = ResultCreate(
        case_id=1,
        case=ResultCreateCase(
            title="title_example",
            suite_title="suite_title_example",
            description="description_example",
            preconditions="preconditions_example",
            postconditions="postconditions_example",
            layer="layer_example",
            severity="severity_example",
        ),
        status="in_progress",
        start_time=0,
        time=0,
        time_ms=0,
        defect=True,
        attachments=[
            "attachments_example",
        ],
        stacktrace="stacktrace_example",
        comment="comment_example",
        param={
            "key": "key_example",
        },
        steps=[
            TestStepResultCreate(
                position=1,
                status="passed",
                comment="comment_example",
                attachments=[
                    "attachments_example",
                ],
                action="action_example",
                expected_result="expected_result_example",
                data="data_example",
                steps=[
                    {},
                ],
            ),
        ],
        author_id=1,
    ) # ResultCreate | 

    # example passing only required values which don't have defaults set
    try:
        # Create test run result.
        api_response = api_instance.create_result(code, id, result_create)
        pprint(api_response)
    except qaseio.ApiException as e:
        print("Exception when calling ResultsApi->create_result: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **code** | **str**| Code of project, where to search entities. |
 **id** | **int**| Identifier. |
 **result_create** | [**ResultCreate**](ResultCreate.md)|  |

### Return type

[**CreateResult200Response**](CreateResult200Response.md)

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
> Response create_result_bulk(code, id, result_create_bulk)

Bulk create test run result.

This method allows to create a lot of test run result at once.  If you try to send more than 2,000 results in a single bulk request, you will receive an error with code 413 - Payload Too Large.  If there is no free space left in your team account, when attempting to upload an attachment, e.g., through reporters, you will receive an error with code 507 - Insufficient Storage. 

### Example

* Api Key Authentication (TokenAuth):

```python
import time
import qaseio
from qaseio.api import results_api
from qaseio.model.response import Response
from qaseio.model.result_create_bulk import ResultCreateBulk
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
    api_instance = results_api.ResultsApi(api_client)
    code = "code_example" # str | Code of project, where to search entities.
    id = 1 # int | Identifier.
    result_create_bulk = ResultCreateBulk(
        results=[
            ResultCreate(
                case_id=1,
                case=ResultCreateCase(
                    title="title_example",
                    suite_title="suite_title_example",
                    description="description_example",
                    preconditions="preconditions_example",
                    postconditions="postconditions_example",
                    layer="layer_example",
                    severity="severity_example",
                ),
                status="in_progress",
                start_time=0,
                time=0,
                time_ms=0,
                defect=True,
                attachments=[
                    "attachments_example",
                ],
                stacktrace="stacktrace_example",
                comment="comment_example",
                param={
                    "key": "key_example",
                },
                steps=[
                    TestStepResultCreate(
                        position=1,
                        status="passed",
                        comment="comment_example",
                        attachments=[
                            "attachments_example",
                        ],
                        action="action_example",
                        expected_result="expected_result_example",
                        data="data_example",
                        steps=[
                            {},
                        ],
                    ),
                ],
                author_id=1,
            ),
        ],
    ) # ResultCreateBulk | 

    # example passing only required values which don't have defaults set
    try:
        # Bulk create test run result.
        api_response = api_instance.create_result_bulk(code, id, result_create_bulk)
        pprint(api_response)
    except qaseio.ApiException as e:
        print("Exception when calling ResultsApi->create_result_bulk: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **code** | **str**| Code of project, where to search entities. |
 **id** | **int**| Identifier. |
 **result_create_bulk** | [**ResultCreateBulk**](ResultCreateBulk.md)|  |

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

Delete test run result.

This method allows to delete test run result. 

### Example

* Api Key Authentication (TokenAuth):

```python
import time
import qaseio
from qaseio.api import results_api
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
    api_instance = results_api.ResultsApi(api_client)
    code = "code_example" # str | Code of project, where to search entities.
    id = 1 # int | Identifier.
    hash = "hash_example" # str | Hash.

    # example passing only required values which don't have defaults set
    try:
        # Delete test run result.
        api_response = api_instance.delete_result(code, id, hash)
        pprint(api_response)
    except qaseio.ApiException as e:
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

Get test run result by code.

This method allows to retrieve a specific test run result by Hash. 

### Example

* Api Key Authentication (TokenAuth):

```python
import time
import qaseio
from qaseio.api import results_api
from qaseio.model.result_response import ResultResponse
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
    api_instance = results_api.ResultsApi(api_client)
    code = "code_example" # str | Code of project, where to search entities.
    hash = "hash_example" # str | Hash.

    # example passing only required values which don't have defaults set
    try:
        # Get test run result by code.
        api_response = api_instance.get_result(code, hash)
        pprint(api_response)
    except qaseio.ApiException as e:
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
> ResultListResponse get_results(code)

Get all test run results.

This method allows to retrieve all test run results stored in selected project. 

### Example

* Api Key Authentication (TokenAuth):

```python
import time
import qaseio
from qaseio.api import results_api
from qaseio.model.result_list_response import ResultListResponse
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
    api_instance = results_api.ResultsApi(api_client)
    code = "code_example" # str | Code of project, where to search entities.
    status = "status_example" # str | A single test run result status. Possible values: in_progress, passed, failed, blocked, skipped, invalid.  (optional)
    run = "run_example" # str | A list of run IDs separated by comma. (optional)
    case_id = "case_id_example" # str | A list of case IDs separated by comma. (optional)
    member = "member_example" # str | A list of member IDs separated by comma. (optional)
    api = True # bool |  (optional)
    from_end_time = "from_end_time_example" # str | Will return all results created after provided datetime. Allowed format: `Y-m-d H:i:s`.  (optional)
    to_end_time = "to_end_time_example" # str | Will return all results created before provided datetime. Allowed format: `Y-m-d H:i:s`.  (optional)
    limit = 10 # int | A number of entities in result set. (optional) if omitted the server will use the default value of 10
    offset = 0 # int | How many entities should be skipped. (optional) if omitted the server will use the default value of 0

    # example passing only required values which don't have defaults set
    try:
        # Get all test run results.
        api_response = api_instance.get_results(code)
        pprint(api_response)
    except qaseio.ApiException as e:
        print("Exception when calling ResultsApi->get_results: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get all test run results.
        api_response = api_instance.get_results(code, status=status, run=run, case_id=case_id, member=member, api=api, from_end_time=from_end_time, to_end_time=to_end_time, limit=limit, offset=offset)
        pprint(api_response)
    except qaseio.ApiException as e:
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
 **limit** | **int**| A number of entities in result set. | [optional] if omitted the server will use the default value of 10
 **offset** | **int**| How many entities should be skipped. | [optional] if omitted the server will use the default value of 0

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

Update test run result.

This method allows to update test run result. 

### Example

* Api Key Authentication (TokenAuth):

```python
import time
import qaseio
from qaseio.api import results_api
from qaseio.model.result_update import ResultUpdate
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
    api_instance = results_api.ResultsApi(api_client)
    code = "code_example" # str | Code of project, where to search entities.
    id = 1 # int | Identifier.
    hash = "hash_example" # str | Hash.
    result_update = ResultUpdate(
        status="in_progress",
        time_ms=0,
        defect=True,
        attachments=[
            "attachments_example",
        ],
        stacktrace="stacktrace_example",
        comment="comment_example",
        steps=[
            TestStepResultCreate(
                position=1,
                status="passed",
                comment="comment_example",
                attachments=[
                    "attachments_example",
                ],
                action="action_example",
                expected_result="expected_result_example",
                data="data_example",
                steps=[
                    {},
                ],
            ),
        ],
    ) # ResultUpdate | 

    # example passing only required values which don't have defaults set
    try:
        # Update test run result.
        api_response = api_instance.update_result(code, id, hash, result_update)
        pprint(api_response)
    except qaseio.ApiException as e:
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

