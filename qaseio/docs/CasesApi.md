# qaseio.CasesApi

All URIs are relative to *https://api.qase.io/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**bulk**](CasesApi.md#bulk) | **POST** /case/{code}/bulk | Create test cases in bulk.
[**create_case**](CasesApi.md#create_case) | **POST** /case/{code} | Create a new test case.
[**delete_case**](CasesApi.md#delete_case) | **DELETE** /case/{code}/{id} | Delete test case.
[**get_case**](CasesApi.md#get_case) | **GET** /case/{code}/{id} | Get a specific test case.
[**get_cases**](CasesApi.md#get_cases) | **GET** /case/{code} | Get all test cases.
[**update_case**](CasesApi.md#update_case) | **PATCH** /case/{code}/{id} | Update test case.


# **bulk**
> Bulk200Response bulk(code, bulk_request)

Create test cases in bulk.

This method allows to bulk create new test cases in a project. 

### Example

* Api Key Authentication (TokenAuth):

```python
import time
import qaseio
from qaseio.api import cases_api
from qaseio.model.bulk200_response import Bulk200Response
from qaseio.model.bulk_request import BulkRequest
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
    api_instance = cases_api.CasesApi(api_client)
    code = "code_example" # str | Code of project, where to search entities.
    bulk_request = BulkRequest(
        cases=[
            BulkRequestCasesInner(None),
        ],
    ) # BulkRequest | 

    # example passing only required values which don't have defaults set
    try:
        # Create test cases in bulk.
        api_response = api_instance.bulk(code, bulk_request)
        pprint(api_response)
    except qaseio.ApiException as e:
        print("Exception when calling CasesApi->bulk: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **code** | **str**| Code of project, where to search entities. |
 **bulk_request** | [**BulkRequest**](BulkRequest.md)|  |

### Return type

[**Bulk200Response**](Bulk200Response.md)

### Authorization

[TokenAuth](../README.md#TokenAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | List of IDs of the created cases. |  -  |
**400** | Bad Request. |  -  |
**401** | Unauthorized. |  -  |
**403** | Forbidden. |  -  |
**404** | Not Found. |  -  |
**422** | Unprocessable Entity. |  -  |
**429** | Too Many Requests. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_case**
> IdResponse create_case(code, test_case_create)

Create a new test case.

This method allows to create a new test case in selected project. 

### Example

* Api Key Authentication (TokenAuth):

```python
import time
import qaseio
from qaseio.api import cases_api
from qaseio.model.test_case_create import TestCaseCreate
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
    api_instance = cases_api.CasesApi(api_client)
    code = "code_example" # str | Code of project, where to search entities.
    test_case_create = TestCaseCreate(
        description="description_example",
        preconditions="preconditions_example",
        postconditions="postconditions_example",
        title="title_example",
        severity=1,
        priority=1,
        behavior=1,
        type=1,
        layer=1,
        is_flaky=1,
        suite_id=1,
        milestone_id=1,
        automation=1,
        status=1,
        attachments=AttachmentHashList([
            "attachments_example",
        ]),
        steps=[
            TestStepCreate(
                action="action_example",
                expected_result="expected_result_example",
                data="data_example",
                position=1,
                attachments=AttachmentHashList([
                    "attachments_example",
                ]),
                steps=[
                    {},
                ],
            ),
        ],
        tags=[
            "tags_example",
        ],
        params={
            "key": [
                "key_example",
            ],
        },
        custom_field={
            "key": "key_example",
        },
        created_at="created_at_example",
        updated_at="updated_at_example",
    ) # TestCaseCreate | 

    # example passing only required values which don't have defaults set
    try:
        # Create a new test case.
        api_response = api_instance.create_case(code, test_case_create)
        pprint(api_response)
    except qaseio.ApiException as e:
        print("Exception when calling CasesApi->create_case: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **code** | **str**| Code of project, where to search entities. |
 **test_case_create** | [**TestCaseCreate**](TestCaseCreate.md)|  |

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

# **delete_case**
> IdResponse delete_case(code, id)

Delete test case.

This method completely deletes a test case from repository. 

### Example

* Api Key Authentication (TokenAuth):

```python
import time
import qaseio
from qaseio.api import cases_api
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
    api_instance = cases_api.CasesApi(api_client)
    code = "code_example" # str | Code of project, where to search entities.
    id = 1 # int | Identifier.

    # example passing only required values which don't have defaults set
    try:
        # Delete test case.
        api_response = api_instance.delete_case(code, id)
        pprint(api_response)
    except qaseio.ApiException as e:
        print("Exception when calling CasesApi->delete_case: %s\n" % e)
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
**200** | A Test Case. |  -  |
**400** | Bad Request. |  -  |
**401** | Unauthorized. |  -  |
**403** | Forbidden. |  -  |
**404** | Not Found. |  -  |
**422** | Unprocessable Entity. |  -  |
**429** | Too Many Requests. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_case**
> TestCaseResponse get_case(code, id)

Get a specific test case.

This method allows to retrieve a specific test case. 

### Example

* Api Key Authentication (TokenAuth):

```python
import time
import qaseio
from qaseio.api import cases_api
from qaseio.model.test_case_response import TestCaseResponse
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
    api_instance = cases_api.CasesApi(api_client)
    code = "code_example" # str | Code of project, where to search entities.
    id = 1 # int | Identifier.

    # example passing only required values which don't have defaults set
    try:
        # Get a specific test case.
        api_response = api_instance.get_case(code, id)
        pprint(api_response)
    except qaseio.ApiException as e:
        print("Exception when calling CasesApi->get_case: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **code** | **str**| Code of project, where to search entities. |
 **id** | **int**| Identifier. |

### Return type

[**TestCaseResponse**](TestCaseResponse.md)

### Authorization

[TokenAuth](../README.md#TokenAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A Test Case. |  -  |
**400** | Bad Request. |  -  |
**401** | Unauthorized. |  -  |
**403** | Forbidden. |  -  |
**404** | Not Found. |  -  |
**422** | Unprocessable Entity. |  -  |
**429** | Too Many Requests. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_cases**
> TestCaseListResponse get_cases(code)

Get all test cases.

This method allows to retrieve all test cases stored in selected project. 

### Example

* Api Key Authentication (TokenAuth):

```python
import time
import qaseio
from qaseio.api import cases_api
from qaseio.model.test_case_list_response import TestCaseListResponse
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
    api_instance = cases_api.CasesApi(api_client)
    code = "code_example" # str | Code of project, where to search entities.
    search = "search_example" # str | Provide a string that will be used to search by name. (optional)
    milestone_id = 1 # int | ID of milestone. (optional)
    suite_id = 1 # int | ID of test suite. (optional)
    severity = "severity_example" # str | A list of severity values separated by comma. Possible values: undefined, blocker, critical, major, normal, minor, trivial  (optional)
    priority = "priority_example" # str | A list of priority values separated by comma. Possible values: undefined, high, medium, low  (optional)
    type = "type_example" # str | A list of type values separated by comma. Possible values: other, functional smoke, regression, security, usability, performance, acceptance  (optional)
    behavior = "behavior_example" # str | A list of behavior values separated by comma. Possible values: undefined, positive negative, destructive  (optional)
    automation = "automation_example" # str | A list of values separated by comma. Possible values: is-not-automated, automated to-be-automated  (optional)
    status = "status_example" # str | A list of values separated by comma. Possible values: actual, draft deprecated  (optional)
    limit = 10 # int | A number of entities in result set. (optional) if omitted the server will use the default value of 10
    offset = 0 # int | How many entities should be skipped. (optional) if omitted the server will use the default value of 0

    # example passing only required values which don't have defaults set
    try:
        # Get all test cases.
        api_response = api_instance.get_cases(code)
        pprint(api_response)
    except qaseio.ApiException as e:
        print("Exception when calling CasesApi->get_cases: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get all test cases.
        api_response = api_instance.get_cases(code, search=search, milestone_id=milestone_id, suite_id=suite_id, severity=severity, priority=priority, type=type, behavior=behavior, automation=automation, status=status, limit=limit, offset=offset)
        pprint(api_response)
    except qaseio.ApiException as e:
        print("Exception when calling CasesApi->get_cases: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **code** | **str**| Code of project, where to search entities. |
 **search** | **str**| Provide a string that will be used to search by name. | [optional]
 **milestone_id** | **int**| ID of milestone. | [optional]
 **suite_id** | **int**| ID of test suite. | [optional]
 **severity** | **str**| A list of severity values separated by comma. Possible values: undefined, blocker, critical, major, normal, minor, trivial  | [optional]
 **priority** | **str**| A list of priority values separated by comma. Possible values: undefined, high, medium, low  | [optional]
 **type** | **str**| A list of type values separated by comma. Possible values: other, functional smoke, regression, security, usability, performance, acceptance  | [optional]
 **behavior** | **str**| A list of behavior values separated by comma. Possible values: undefined, positive negative, destructive  | [optional]
 **automation** | **str**| A list of values separated by comma. Possible values: is-not-automated, automated to-be-automated  | [optional]
 **status** | **str**| A list of values separated by comma. Possible values: actual, draft deprecated  | [optional]
 **limit** | **int**| A number of entities in result set. | [optional] if omitted the server will use the default value of 10
 **offset** | **int**| How many entities should be skipped. | [optional] if omitted the server will use the default value of 0

### Return type

[**TestCaseListResponse**](TestCaseListResponse.md)

### Authorization

[TokenAuth](../README.md#TokenAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A list of all cases. |  -  |
**400** | Bad Request. |  -  |
**401** | Unauthorized. |  -  |
**403** | Forbidden. |  -  |
**404** | Not Found. |  -  |
**429** | Too Many Requests. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_case**
> IdResponse update_case(code, id, test_case_update)

Update test case.

This method updates a test case. 

### Example

* Api Key Authentication (TokenAuth):

```python
import time
import qaseio
from qaseio.api import cases_api
from qaseio.model.test_case_update import TestCaseUpdate
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
    api_instance = cases_api.CasesApi(api_client)
    code = "code_example" # str | Code of project, where to search entities.
    id = 1 # int | Identifier.
    test_case_update = TestCaseUpdate(
        description="description_example",
        preconditions="preconditions_example",
        postconditions="postconditions_example",
        title="title_example",
        severity=1,
        priority=1,
        behavior=1,
        type=1,
        layer=1,
        is_flaky=1,
        suite_id=1,
        milestone_id=1,
        automation=1,
        status=1,
        attachments=AttachmentHashList([
            "attachments_example",
        ]),
        steps=[
            TestStepCreate(
                action="action_example",
                expected_result="expected_result_example",
                data="data_example",
                position=1,
                attachments=AttachmentHashList([
                    "attachments_example",
                ]),
                steps=[
                    {},
                ],
            ),
        ],
        tags=[
            "tags_example",
        ],
        params={
            "key": [
                "key_example",
            ],
        },
        custom_field={
            "key": "key_example",
        },
    ) # TestCaseUpdate | 

    # example passing only required values which don't have defaults set
    try:
        # Update test case.
        api_response = api_instance.update_case(code, id, test_case_update)
        pprint(api_response)
    except qaseio.ApiException as e:
        print("Exception when calling CasesApi->update_case: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **code** | **str**| Code of project, where to search entities. |
 **id** | **int**| Identifier. |
 **test_case_update** | [**TestCaseUpdate**](TestCaseUpdate.md)|  |

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
**200** | A Test Case. |  -  |
**400** | Bad Request. |  -  |
**401** | Unauthorized. |  -  |
**403** | Forbidden. |  -  |
**404** | Not Found. |  -  |
**422** | Unprocessable Entity. |  -  |
**429** | Too Many Requests. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

