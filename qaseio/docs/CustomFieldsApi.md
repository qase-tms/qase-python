# qaseio.CustomFieldsApi

All URIs are relative to *https://api.qase.io/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_custom_field**](CustomFieldsApi.md#create_custom_field) | **POST** /custom_field | Create new Custom Field.
[**delete_custom_field**](CustomFieldsApi.md#delete_custom_field) | **DELETE** /custom_field/{id} | Delete Custom Field by id.
[**get_custom_field**](CustomFieldsApi.md#get_custom_field) | **GET** /custom_field/{id} | Get Custom Field by id.
[**get_custom_fields**](CustomFieldsApi.md#get_custom_fields) | **GET** /custom_field | Get all Custom Fields.
[**update_custom_field**](CustomFieldsApi.md#update_custom_field) | **PATCH** /custom_field/{id} | Update Custom Field by id.


# **create_custom_field**
> IdResponse create_custom_field(custom_field_create)

Create new Custom Field.

This method allows to create custom field. 

### Example

* Api Key Authentication (TokenAuth):

```python
import time
import qaseio
from qaseio.api import custom_fields_api
from qaseio.model.custom_field_create import CustomFieldCreate
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
    api_instance = custom_fields_api.CustomFieldsApi(api_client)
    custom_field_create = CustomFieldCreate(
        title="title_example",
        value=[
            CustomFieldCreateValueInner(
                id=1,
                title="title_example",
            ),
        ],
        entity=0,
        type=0,
        placeholder="placeholder_example",
        default_value="default_value_example",
        is_filterable=True,
        is_visible=True,
        is_required=True,
        is_enabled_for_all_projects=True,
        projects_codes=[
            "projects_codes_example",
        ],
    ) # CustomFieldCreate | 

    # example passing only required values which don't have defaults set
    try:
        # Create new Custom Field.
        api_response = api_instance.create_custom_field(custom_field_create)
        pprint(api_response)
    except qaseio.ApiException as e:
        print("Exception when calling CustomFieldsApi->create_custom_field: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **custom_field_create** | [**CustomFieldCreate**](CustomFieldCreate.md)|  |

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
**200** | Created Custom Field id. |  -  |
**400** | Bad Request. |  -  |
**401** | Unauthorized. |  -  |
**403** | Forbidden. |  -  |
**422** | Unprocessable Entity. |  -  |
**429** | Too Many Requests. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_custom_field**
> Response delete_custom_field(id)

Delete Custom Field by id.

This method allows to delete custom field. 

### Example

* Api Key Authentication (TokenAuth):

```python
import time
import qaseio
from qaseio.api import custom_fields_api
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
    api_instance = custom_fields_api.CustomFieldsApi(api_client)
    id = 1 # int | Identifier.

    # example passing only required values which don't have defaults set
    try:
        # Delete Custom Field by id.
        api_response = api_instance.delete_custom_field(id)
        pprint(api_response)
    except qaseio.ApiException as e:
        print("Exception when calling CustomFieldsApi->delete_custom_field: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
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
**200** | Custom Field removal result. |  -  |
**400** | Bad Request. |  -  |
**401** | Unauthorized. |  -  |
**403** | Forbidden. |  -  |
**404** | Not Found. |  -  |
**429** | Too Many Requests. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_custom_field**
> CustomFieldResponse get_custom_field(id)

Get Custom Field by id.

This method allows to retrieve custom field. 

### Example

* Api Key Authentication (TokenAuth):

```python
import time
import qaseio
from qaseio.api import custom_fields_api
from qaseio.model.custom_field_response import CustomFieldResponse
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
    api_instance = custom_fields_api.CustomFieldsApi(api_client)
    id = 1 # int | Identifier.

    # example passing only required values which don't have defaults set
    try:
        # Get Custom Field by id.
        api_response = api_instance.get_custom_field(id)
        pprint(api_response)
    except qaseio.ApiException as e:
        print("Exception when calling CustomFieldsApi->get_custom_field: %s\n" % e)
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

# **get_custom_fields**
> CustomFieldsResponse get_custom_fields()

Get all Custom Fields.

This method allows to retrieve and filter custom fields. 

### Example

* Api Key Authentication (TokenAuth):

```python
import time
import qaseio
from qaseio.api import custom_fields_api
from qaseio.model.custom_fields_response import CustomFieldsResponse
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
    api_instance = custom_fields_api.CustomFieldsApi(api_client)
    entity = "case" # str |  (optional)
    type = "string" # str |  (optional)
    limit = 10 # int | A number of entities in result set. (optional) if omitted the server will use the default value of 10
    offset = 0 # int | How many entities should be skipped. (optional) if omitted the server will use the default value of 0

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get all Custom Fields.
        api_response = api_instance.get_custom_fields(entity=entity, type=type, limit=limit, offset=offset)
        pprint(api_response)
    except qaseio.ApiException as e:
        print("Exception when calling CustomFieldsApi->get_custom_fields: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **entity** | **str**|  | [optional]
 **type** | **str**|  | [optional]
 **limit** | **int**| A number of entities in result set. | [optional] if omitted the server will use the default value of 10
 **offset** | **int**| How many entities should be skipped. | [optional] if omitted the server will use the default value of 0

### Return type

[**CustomFieldsResponse**](CustomFieldsResponse.md)

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

# **update_custom_field**
> Response update_custom_field(id, custom_field_update)

Update Custom Field by id.

This method allows to update custom field. 

### Example

* Api Key Authentication (TokenAuth):

```python
import time
import qaseio
from qaseio.api import custom_fields_api
from qaseio.model.response import Response
from qaseio.model.custom_field_update import CustomFieldUpdate
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
    api_instance = custom_fields_api.CustomFieldsApi(api_client)
    id = 1 # int | Identifier.
    custom_field_update = CustomFieldUpdate(
        title="title_example",
        value=[
            CustomFieldCreateValueInner(
                id=1,
                title="title_example",
            ),
        ],
        replace_values={
            "key": "key_example",
        },
        placeholder="placeholder_example",
        default_value="default_value_example",
        is_filterable=True,
        is_visible=True,
        is_required=True,
        is_enabled_for_all_projects=True,
        projects_codes=[
            "projects_codes_example",
        ],
    ) # CustomFieldUpdate | 

    # example passing only required values which don't have defaults set
    try:
        # Update Custom Field by id.
        api_response = api_instance.update_custom_field(id, custom_field_update)
        pprint(api_response)
    except qaseio.ApiException as e:
        print("Exception when calling CustomFieldsApi->update_custom_field: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**| Identifier. |
 **custom_field_update** | [**CustomFieldUpdate**](CustomFieldUpdate.md)|  |

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
**200** | Custom Field update result. |  -  |
**400** | Bad Request. |  -  |
**401** | Unauthorized. |  -  |
**403** | Forbidden. |  -  |
**404** | Not Found. |  -  |
**422** | Unprocessable Entity. |  -  |
**429** | Too Many Requests. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

