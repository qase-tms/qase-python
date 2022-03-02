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
> InlineResponse200 create_result(body, code, id)

Create test run result.

This method allows to create test run result by Run Id. 

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
api_instance = qaseio.ResultsApi(qaseio.ApiClient(configuration))
body = qaseio.ResultCreate() # ResultCreate | 
code = 'code_example' # str | Code of project, where to search entities.
id = 56 # int | Identifier.

try:
    # Create test run result.
    api_response = api_instance.create_result(body, code, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ResultsApi->create_result: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ResultCreate**](ResultCreate.md)|  | 
 **code** | **str**| Code of project, where to search entities. | 
 **id** | **int**| Identifier. | 

### Return type

[**InlineResponse200**](InlineResponse200.md)

### Authorization

[TokenAuth](../README.md#TokenAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_result_bulk**
> Response create_result_bulk(body, code, id)

Bulk create test run result.

This method allows to create a lot of test run result at once. 

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
api_instance = qaseio.ResultsApi(qaseio.ApiClient(configuration))
body = qaseio.ResultCreateBulk() # ResultCreateBulk | 
code = 'code_example' # str | Code of project, where to search entities.
id = 56 # int | Identifier.

try:
    # Bulk create test run result.
    api_response = api_instance.create_result_bulk(body, code, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ResultsApi->create_result_bulk: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ResultCreateBulk**](ResultCreateBulk.md)|  | 
 **code** | **str**| Code of project, where to search entities. | 
 **id** | **int**| Identifier. | 

### Return type

[**Response**](Response.md)

### Authorization

[TokenAuth](../README.md#TokenAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_result**
> HashResponse delete_result(code, id, hash)

Delete test run result.

This method allows to delete test run result. 

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
api_instance = qaseio.ResultsApi(qaseio.ApiClient(configuration))
code = 'code_example' # str | Code of project, where to search entities.
id = 56 # int | Identifier.
hash = 'hash_example' # str | Hash.

try:
    # Delete test run result.
    api_response = api_instance.delete_result(code, id, hash)
    pprint(api_response)
except ApiException as e:
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

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_result**
> ResultResponse get_result(code, hash)

Get test run result by code.

This method allows to retrieve a specific test run result by Hash. 

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
api_instance = qaseio.ResultsApi(qaseio.ApiClient(configuration))
code = 'code_example' # str | Code of project, where to search entities.
hash = 'hash_example' # str | Hash.

try:
    # Get test run result by code.
    api_response = api_instance.get_result(code, hash)
    pprint(api_response)
except ApiException as e:
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

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_results**
> ResultListResponse get_results(code, filters=filters, limit=limit, offset=offset)

Get all test run results.

This method allows to retrieve all test run results stored in selected project. 

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
api_instance = qaseio.ResultsApi(qaseio.ApiClient(configuration))
code = 'code_example' # str | Code of project, where to search entities.
filters = qaseio.Filters4() # Filters4 |  (optional)
limit = 10 # int | A number of entities in result set. (optional) (default to 10)
offset = 0 # int | How many entities should be skipped. (optional) (default to 0)

try:
    # Get all test run results.
    api_response = api_instance.get_results(code, filters=filters, limit=limit, offset=offset)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ResultsApi->get_results: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **code** | **str**| Code of project, where to search entities. | 
 **filters** | [**Filters4**](.md)|  | [optional] 
 **limit** | **int**| A number of entities in result set. | [optional] [default to 10]
 **offset** | **int**| How many entities should be skipped. | [optional] [default to 0]

### Return type

[**ResultListResponse**](ResultListResponse.md)

### Authorization

[TokenAuth](../README.md#TokenAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_result**
> HashResponse update_result(body, code, id, hash)

Update test run result.

This method allows to update test run result. 

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
api_instance = qaseio.ResultsApi(qaseio.ApiClient(configuration))
body = qaseio.ResultUpdate() # ResultUpdate | 
code = 'code_example' # str | Code of project, where to search entities.
id = 56 # int | Identifier.
hash = 'hash_example' # str | Hash.

try:
    # Update test run result.
    api_response = api_instance.update_result(body, code, id, hash)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ResultsApi->update_result: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ResultUpdate**](ResultUpdate.md)|  | 
 **code** | **str**| Code of project, where to search entities. | 
 **id** | **int**| Identifier. | 
 **hash** | **str**| Hash. | 

### Return type

[**HashResponse**](HashResponse.md)

### Authorization

[TokenAuth](../README.md#TokenAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

