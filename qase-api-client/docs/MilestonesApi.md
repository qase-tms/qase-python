# qase.api_client_v1.MilestonesApi

All URIs are relative to *https://api.qase.io/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_milestone**](MilestonesApi.md#create_milestone) | **POST** /milestone/{code} | Create a new milestone
[**delete_milestone**](MilestonesApi.md#delete_milestone) | **DELETE** /milestone/{code}/{id} | Delete milestone
[**get_milestone**](MilestonesApi.md#get_milestone) | **GET** /milestone/{code}/{id} | Get a specific milestone
[**get_milestones**](MilestonesApi.md#get_milestones) | **GET** /milestone/{code} | Get all milestones
[**update_milestone**](MilestonesApi.md#update_milestone) | **PATCH** /milestone/{code}/{id} | Update milestone


# **create_milestone**
> IdResponse create_milestone(code, milestone_create)

Create a new milestone

This method allows to create a milestone in selected project. 

### Example

* Api Key Authentication (TokenAuth):

```python
import qase.api_client_v1
from qase.api_client_v1.models.id_response import IdResponse
from qase.api_client_v1.models.milestone_create import MilestoneCreate
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
    api_instance = qase.api_client_v1.MilestonesApi(api_client)
    code = 'code_example' # str | Code of project, where to search entities.
    milestone_create = qase.api_client_v1.MilestoneCreate() # MilestoneCreate | 

    try:
        # Create a new milestone
        api_response = api_instance.create_milestone(code, milestone_create)
        print("The response of MilestonesApi->create_milestone:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MilestonesApi->create_milestone: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **code** | **str**| Code of project, where to search entities. | 
 **milestone_create** | [**MilestoneCreate**](MilestoneCreate.md)|  | 

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

# **delete_milestone**
> IdResponse delete_milestone(code, id)

Delete milestone

This method completely deletes a milestone from repository. 

### Example

* Api Key Authentication (TokenAuth):

```python
import qase.api_client_v1
from qase.api_client_v1.models.id_response import IdResponse
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
    api_instance = qase.api_client_v1.MilestonesApi(api_client)
    code = 'code_example' # str | Code of project, where to search entities.
    id = 56 # int | Identifier.

    try:
        # Delete milestone
        api_response = api_instance.delete_milestone(code, id)
        print("The response of MilestonesApi->delete_milestone:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MilestonesApi->delete_milestone: %s\n" % e)
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

# **get_milestone**
> MilestoneResponse get_milestone(code, id)

Get a specific milestone

This method allows to retrieve a specific milestone. 

### Example

* Api Key Authentication (TokenAuth):

```python
import qase.api_client_v1
from qase.api_client_v1.models.milestone_response import MilestoneResponse
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
    api_instance = qase.api_client_v1.MilestonesApi(api_client)
    code = 'code_example' # str | Code of project, where to search entities.
    id = 56 # int | Identifier.

    try:
        # Get a specific milestone
        api_response = api_instance.get_milestone(code, id)
        print("The response of MilestonesApi->get_milestone:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MilestonesApi->get_milestone: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **code** | **str**| Code of project, where to search entities. | 
 **id** | **int**| Identifier. | 

### Return type

[**MilestoneResponse**](MilestoneResponse.md)

### Authorization

[TokenAuth](../README.md#TokenAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A Milestone. |  -  |
**400** | Bad Request. |  -  |
**401** | Unauthorized. |  -  |
**403** | Forbidden. |  -  |
**404** | Not Found. |  -  |
**429** | Too Many Requests. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_milestones**
> MilestoneListResponse get_milestones(code, search=search, limit=limit, offset=offset)

Get all milestones

This method allows to retrieve all milestones stored in selected project. 

### Example

* Api Key Authentication (TokenAuth):

```python
import qase.api_client_v1
from qase.api_client_v1.models.milestone_list_response import MilestoneListResponse
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
    api_instance = qase.api_client_v1.MilestonesApi(api_client)
    code = 'code_example' # str | Code of project, where to search entities.
    search = 'search_example' # str | Provide a string that will be used to search by name. (optional)
    limit = 10 # int | A number of entities in result set. (optional) (default to 10)
    offset = 0 # int | How many entities should be skipped. (optional) (default to 0)

    try:
        # Get all milestones
        api_response = api_instance.get_milestones(code, search=search, limit=limit, offset=offset)
        print("The response of MilestonesApi->get_milestones:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MilestonesApi->get_milestones: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **code** | **str**| Code of project, where to search entities. | 
 **search** | **str**| Provide a string that will be used to search by name. | [optional] 
 **limit** | **int**| A number of entities in result set. | [optional] [default to 10]
 **offset** | **int**| How many entities should be skipped. | [optional] [default to 0]

### Return type

[**MilestoneListResponse**](MilestoneListResponse.md)

### Authorization

[TokenAuth](../README.md#TokenAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A list of all milestones. |  -  |
**400** | Bad Request. |  -  |
**401** | Unauthorized. |  -  |
**403** | Forbidden. |  -  |
**404** | Not Found. |  -  |
**429** | Too Many Requests. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_milestone**
> IdResponse update_milestone(code, id, milestone_update)

Update milestone

This method updates a milestone. 

### Example

* Api Key Authentication (TokenAuth):

```python
import qase.api_client_v1
from qase.api_client_v1.models.id_response import IdResponse
from qase.api_client_v1.models.milestone_update import MilestoneUpdate
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
    api_instance = qase.api_client_v1.MilestonesApi(api_client)
    code = 'code_example' # str | Code of project, where to search entities.
    id = 56 # int | Identifier.
    milestone_update = qase.api_client_v1.MilestoneUpdate() # MilestoneUpdate | 

    try:
        # Update milestone
        api_response = api_instance.update_milestone(code, id, milestone_update)
        print("The response of MilestonesApi->update_milestone:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MilestonesApi->update_milestone: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **code** | **str**| Code of project, where to search entities. | 
 **id** | **int**| Identifier. | 
 **milestone_update** | [**MilestoneUpdate**](MilestoneUpdate.md)|  | 

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

