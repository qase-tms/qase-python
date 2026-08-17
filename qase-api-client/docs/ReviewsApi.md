# qase.api_client_v1.ReviewsApi

All URIs are relative to *https://api.qase.io/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**bulk_create_reviews**](ReviewsApi.md#bulk_create_reviews) | **POST** /review/{code}/bulk | Create reviews in bulk
[**create_review**](ReviewsApi.md#create_review) | **POST** /review/{code} | Create a new review
[**delete_review**](ReviewsApi.md#delete_review) | **DELETE** /review/{code}/{id} | Delete review
[**get_review**](ReviewsApi.md#get_review) | **GET** /review/{code}/{id} | Get a specific review
[**get_reviews**](ReviewsApi.md#get_reviews) | **GET** /review/{code} | Get all reviews
[**update_review**](ReviewsApi.md#update_review) | **PATCH** /review/{code}/{id} | Update review


# **bulk_create_reviews**
> ReviewBulkResponse bulk_create_reviews(code, review_bulk)

Create reviews in bulk

This method allows to submit multiple test cases for review in one request.

Returns an error if test case review is disabled in the project settings.


### Example

* Api Key Authentication (TokenAuth):

```python
import qase.api_client_v1
from qase.api_client_v1.models.review_bulk import ReviewBulk
from qase.api_client_v1.models.review_bulk_response import ReviewBulkResponse
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
    api_instance = qase.api_client_v1.ReviewsApi(api_client)
    code = 'code_example' # str | Code of project, where to search entities.
    review_bulk = qase.api_client_v1.ReviewBulk() # ReviewBulk | 

    try:
        # Create reviews in bulk
        api_response = api_instance.bulk_create_reviews(code, review_bulk)
        print("The response of ReviewsApi->bulk_create_reviews:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ReviewsApi->bulk_create_reviews: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **code** | **str**| Code of project, where to search entities. | 
 **review_bulk** | [**ReviewBulk**](ReviewBulk.md)|  | 

### Return type

[**ReviewBulkResponse**](ReviewBulkResponse.md)

### Authorization

[TokenAuth](../README.md#TokenAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Per-item outcomes for the submitted reviews. |  -  |
**400** | Bad Request. |  -  |
**401** | Unauthorized. |  -  |
**402** | Payment Required. |  -  |
**403** | Forbidden. |  -  |
**404** | Not Found. |  -  |
**422** | Unprocessable Entity. |  -  |
**429** | Too Many Requests. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_review**
> IdResponse create_review(code, review_create)

Create a new review

This method allows to submit a test case for review in selected project.

Returns an error if test case review is disabled in the project settings.


### Example

* Api Key Authentication (TokenAuth):

```python
import qase.api_client_v1
from qase.api_client_v1.models.id_response import IdResponse
from qase.api_client_v1.models.review_create import ReviewCreate
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
    api_instance = qase.api_client_v1.ReviewsApi(api_client)
    code = 'code_example' # str | Code of project, where to search entities.
    review_create = qase.api_client_v1.ReviewCreate() # ReviewCreate | 

    try:
        # Create a new review
        api_response = api_instance.create_review(code, review_create)
        print("The response of ReviewsApi->create_review:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ReviewsApi->create_review: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **code** | **str**| Code of project, where to search entities. | 
 **review_create** | [**ReviewCreate**](ReviewCreate.md)|  | 

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
**402** | Payment Required. |  -  |
**403** | Forbidden. |  -  |
**404** | Not Found. |  -  |
**422** | Unprocessable Entity. |  -  |
**429** | Too Many Requests. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_review**
> IdResponse delete_review(code, id)

Delete review

This method allows to delete a review. Merged reviews cannot be deleted.

Returns an error if test case review is disabled in the project settings.


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
    api_instance = qase.api_client_v1.ReviewsApi(api_client)
    code = 'code_example' # str | Code of project, where to search entities.
    id = 56 # int | Identifier.

    try:
        # Delete review
        api_response = api_instance.delete_review(code, id)
        print("The response of ReviewsApi->delete_review:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ReviewsApi->delete_review: %s\n" % e)
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
**200** | A result. |  -  |
**400** | Bad Request. |  -  |
**401** | Unauthorized. |  -  |
**402** | Payment Required. |  -  |
**403** | Forbidden. |  -  |
**404** | Not Found. |  -  |
**422** | Unprocessable Entity. |  -  |
**429** | Too Many Requests. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_review**
> ReviewResponse get_review(code, id)

Get a specific review

This method allows to retrieve a specific review, including its current
approval status per reviewer.


### Example

* Api Key Authentication (TokenAuth):

```python
import qase.api_client_v1
from qase.api_client_v1.models.review_response import ReviewResponse
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
    api_instance = qase.api_client_v1.ReviewsApi(api_client)
    code = 'code_example' # str | Code of project, where to search entities.
    id = 56 # int | Identifier.

    try:
        # Get a specific review
        api_response = api_instance.get_review(code, id)
        print("The response of ReviewsApi->get_review:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ReviewsApi->get_review: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **code** | **str**| Code of project, where to search entities. | 
 **id** | **int**| Identifier. | 

### Return type

[**ReviewResponse**](ReviewResponse.md)

### Authorization

[TokenAuth](../README.md#TokenAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A Review. |  -  |
**400** | Bad Request. |  -  |
**401** | Unauthorized. |  -  |
**402** | Payment Required. |  -  |
**403** | Forbidden. |  -  |
**404** | Not Found. |  -  |
**429** | Too Many Requests. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_reviews**
> ReviewListResponse get_reviews(code, status=status, type=type, case_id=case_id, author_uuid=author_uuid, reviewer_uuid=reviewer_uuid, search=search, limit=limit, offset=offset)

Get all reviews

This method allows to retrieve all test case reviews stored in selected project.


### Example

* Api Key Authentication (TokenAuth):

```python
import qase.api_client_v1
from qase.api_client_v1.models.review_list_response import ReviewListResponse
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
    api_instance = qase.api_client_v1.ReviewsApi(api_client)
    code = 'code_example' # str | Code of project, where to search entities.
    status = 'status_example' # str |  (optional)
    type = 'type_example' # str |  (optional)
    case_id = 56 # int | Filter reviews by the reviewed test case ID. (optional)
    author_uuid = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | Filter reviews by the author who created them (author UUID). (optional)
    reviewer_uuid = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | Filter reviews by an assigned reviewer (author UUID). (optional)
    search = 'search_example' # str | Provide a string that will be used to search by review title. (optional)
    limit = 10 # int | A number of entities in result set. (optional) (default to 10)
    offset = 0 # int | How many entities should be skipped. (optional) (default to 0)

    try:
        # Get all reviews
        api_response = api_instance.get_reviews(code, status=status, type=type, case_id=case_id, author_uuid=author_uuid, reviewer_uuid=reviewer_uuid, search=search, limit=limit, offset=offset)
        print("The response of ReviewsApi->get_reviews:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ReviewsApi->get_reviews: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **code** | **str**| Code of project, where to search entities. | 
 **status** | **str**|  | [optional] 
 **type** | **str**|  | [optional] 
 **case_id** | **int**| Filter reviews by the reviewed test case ID. | [optional] 
 **author_uuid** | **UUID**| Filter reviews by the author who created them (author UUID). | [optional] 
 **reviewer_uuid** | **UUID**| Filter reviews by an assigned reviewer (author UUID). | [optional] 
 **search** | **str**| Provide a string that will be used to search by review title. | [optional] 
 **limit** | **int**| A number of entities in result set. | [optional] [default to 10]
 **offset** | **int**| How many entities should be skipped. | [optional] [default to 0]

### Return type

[**ReviewListResponse**](ReviewListResponse.md)

### Authorization

[TokenAuth](../README.md#TokenAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A list of all reviews. |  -  |
**400** | Bad Request. |  -  |
**401** | Unauthorized. |  -  |
**402** | Payment Required. |  -  |
**403** | Forbidden. |  -  |
**404** | Not Found. |  -  |
**429** | Too Many Requests. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_review**
> IdResponse update_review(code, id, review_update)

Update review

This method allows to update the assigned reviewers and/or the proposed
test case payload of an open review. The reviewed test case cannot be changed.

Returns an error if test case review is disabled in the project settings,
or if the review is not open.


### Example

* Api Key Authentication (TokenAuth):

```python
import qase.api_client_v1
from qase.api_client_v1.models.id_response import IdResponse
from qase.api_client_v1.models.review_update import ReviewUpdate
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
    api_instance = qase.api_client_v1.ReviewsApi(api_client)
    code = 'code_example' # str | Code of project, where to search entities.
    id = 56 # int | Identifier.
    review_update = qase.api_client_v1.ReviewUpdate() # ReviewUpdate | 

    try:
        # Update review
        api_response = api_instance.update_review(code, id, review_update)
        print("The response of ReviewsApi->update_review:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ReviewsApi->update_review: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **code** | **str**| Code of project, where to search entities. | 
 **id** | **int**| Identifier. | 
 **review_update** | [**ReviewUpdate**](ReviewUpdate.md)|  | 

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
**402** | Payment Required. |  -  |
**403** | Forbidden. |  -  |
**404** | Not Found. |  -  |
**422** | Unprocessable Entity. |  -  |
**429** | Too Many Requests. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

