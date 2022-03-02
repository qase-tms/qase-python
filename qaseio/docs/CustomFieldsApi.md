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
> IdResponse create_custom_field(body)

Create new Custom Field.

This method allows to create custom field. 

### Example
```python
from __future__ import print_function
import time
import qaseio
from qaseio.rest import ApiException
from pprint import pprint

# Configure API key authorization: TokenAuth
configuration = qaseio.Configuration()
configuration.api_key['Token'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Token'] = 'Bearer'

# create an instance of the API class
api_instance = qaseio.CustomFieldsApi(qaseio.ApiClient(configuration))
body = qaseio.CustomFieldCreate() # CustomFieldCreate | 

try:
    # Create new Custom Field.
    api_response = api_instance.create_custom_field(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CustomFieldsApi->create_custom_field: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**CustomFieldCreate**](CustomFieldCreate.md)|  | 

### Return type

[**IdResponse**](IdResponse.md)

### Authorization

[TokenAuth](../README.md#TokenAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_custom_field**
> Response delete_custom_field(id)

Delete Custom Field by id.

This method allows to delete custom field. 

### Example
```python
from __future__ import print_function
import time
import qaseio
from qaseio.rest import ApiException
from pprint import pprint

# Configure API key authorization: TokenAuth
configuration = qaseio.Configuration()
configuration.api_key['Token'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Token'] = 'Bearer'

# create an instance of the API class
api_instance = qaseio.CustomFieldsApi(qaseio.ApiClient(configuration))
id = 56 # int | Identifier.

try:
    # Delete Custom Field by id.
    api_response = api_instance.delete_custom_field(id)
    pprint(api_response)
except ApiException as e:
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

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_custom_field**
> CustomFieldResponse get_custom_field(id)

Get Custom Field by id.

This method allows to retrieve custom field. 

### Example
```python
from __future__ import print_function
import time
import qaseio
from qaseio.rest import ApiException
from pprint import pprint

# Configure API key authorization: TokenAuth
configuration = qaseio.Configuration()
configuration.api_key['Token'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Token'] = 'Bearer'

# create an instance of the API class
api_instance = qaseio.CustomFieldsApi(qaseio.ApiClient(configuration))
id = 56 # int | Identifier.

try:
    # Get Custom Field by id.
    api_response = api_instance.get_custom_field(id)
    pprint(api_response)
except ApiException as e:
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

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_custom_fields**
> CustomFieldsResponse get_custom_fields(filters=filters, limit=limit, offset=offset)

Get all Custom Fields.

This method allows to retrieve and filter custom fields. 

### Example
```python
from __future__ import print_function
import time
import qaseio
from qaseio.rest import ApiException
from pprint import pprint

# Configure API key authorization: TokenAuth
configuration = qaseio.Configuration()
configuration.api_key['Token'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Token'] = 'Bearer'

# create an instance of the API class
api_instance = qaseio.CustomFieldsApi(qaseio.ApiClient(configuration))
filters = qaseio.Filters1() # Filters1 |  (optional)
limit = 10 # int | A number of entities in result set. (optional) (default to 10)
offset = 0 # int | How many entities should be skipped. (optional) (default to 0)

try:
    # Get all Custom Fields.
    api_response = api_instance.get_custom_fields(filters=filters, limit=limit, offset=offset)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CustomFieldsApi->get_custom_fields: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **filters** | [**Filters1**](.md)|  | [optional] 
 **limit** | **int**| A number of entities in result set. | [optional] [default to 10]
 **offset** | **int**| How many entities should be skipped. | [optional] [default to 0]

### Return type

[**CustomFieldsResponse**](CustomFieldsResponse.md)

### Authorization

[TokenAuth](../README.md#TokenAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_custom_field**
> Response update_custom_field(body, id)

Update Custom Field by id.

This method allows to update custom field. 

### Example
```python
from __future__ import print_function
import time
import qaseio
from qaseio.rest import ApiException
from pprint import pprint

# Configure API key authorization: TokenAuth
configuration = qaseio.Configuration()
configuration.api_key['Token'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Token'] = 'Bearer'

# create an instance of the API class
api_instance = qaseio.CustomFieldsApi(qaseio.ApiClient(configuration))
body = qaseio.CustomFieldUpdate() # CustomFieldUpdate | 
id = 56 # int | Identifier.

try:
    # Update Custom Field by id.
    api_response = api_instance.update_custom_field(body, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CustomFieldsApi->update_custom_field: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**CustomFieldUpdate**](CustomFieldUpdate.md)|  | 
 **id** | **int**| Identifier. | 

### Return type

[**Response**](Response.md)

### Authorization

[TokenAuth](../README.md#TokenAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

