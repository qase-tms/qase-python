# qase.api_client_v2.CustomFieldsApi

All URIs are relative to *https://api.qase.io/v2*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_custom_field_v2**](CustomFieldsApi.md#get_custom_field_v2) | **GET** /custom_field/{id} | Get Custom Field
[**get_custom_fields_v2**](CustomFieldsApi.md#get_custom_fields_v2) | **GET** /custom_field | Get all Custom Fields


# **get_custom_field_v2**
> CustomFieldResponse get_custom_field_v2(id)

Get Custom Field

This method allows to retrieve custom field.


### Example

* Api Key Authentication (TokenAuth):

```python
import qase.api_client_v2
from qase.api_client_v2.models.custom_field_response import CustomFieldResponse
from qase.api_client_v2.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://api.qase.io/v2
# See configuration.py for a list of all supported configuration parameters.
configuration = qase.api_client_v2.Configuration(
    host = "https://api.qase.io/v2"
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
with qase.api_client_v2.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = qase.api_client_v2.CustomFieldsApi(api_client)
    id = 56 # int | Identifier.

    try:
        # Get Custom Field
        api_response = api_instance.get_custom_field_v2(id)
        print("The response of CustomFieldsApi->get_custom_field_v2:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CustomFieldsApi->get_custom_field_v2: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**| Identifier. | 

### Return type

[**CustomFieldResponse**](CustomFieldResponse.md)

### Authorization

[TokenAuth](../README.md#TokenAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A Custom Field. |  -  |
**400** | Bad Request. |  -  |
**401** | Unauthorized. |  -  |
**403** | Forbidden. |  -  |
**404** | Not Found. |  -  |
**429** | Too Many Requests. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_custom_fields_v2**
> CustomFieldListResponse get_custom_fields_v2(entity=entity, type=type, limit=limit, offset=offset)

Get all Custom Fields

This method allows to retrieve and filter custom fields.


### Example

* Api Key Authentication (TokenAuth):

```python
import qase.api_client_v2
from qase.api_client_v2.models.custom_field_list_response import CustomFieldListResponse
from qase.api_client_v2.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://api.qase.io/v2
# See configuration.py for a list of all supported configuration parameters.
configuration = qase.api_client_v2.Configuration(
    host = "https://api.qase.io/v2"
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
with qase.api_client_v2.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = qase.api_client_v2.CustomFieldsApi(api_client)
    entity = 'entity_example' # str |  (optional)
    type = 'type_example' # str |  (optional)
    limit = 10 # int | A number of entities in result set. (optional) (default to 10)
    offset = 0 # int | How many entities should be skipped. (optional) (default to 0)

    try:
        # Get all Custom Fields
        api_response = api_instance.get_custom_fields_v2(entity=entity, type=type, limit=limit, offset=offset)
        print("The response of CustomFieldsApi->get_custom_fields_v2:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CustomFieldsApi->get_custom_fields_v2: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **entity** | **str**|  | [optional] 
 **type** | **str**|  | [optional] 
 **limit** | **int**| A number of entities in result set. | [optional] [default to 10]
 **offset** | **int**| How many entities should be skipped. | [optional] [default to 0]

### Return type

[**CustomFieldListResponse**](CustomFieldListResponse.md)

### Authorization

[TokenAuth](../README.md#TokenAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Custom Field list. |  -  |
**400** | Bad Request. |  -  |
**401** | Unauthorized. |  -  |
**403** | Forbidden. |  -  |
**429** | Too Many Requests. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

