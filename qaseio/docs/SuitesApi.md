# qaseio.SuitesApi

All URIs are relative to *https://api.qase.io/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_suite**](SuitesApi.md#create_suite) | **POST** /suite/{code} | Create a new test suite.
[**delete_suite**](SuitesApi.md#delete_suite) | **DELETE** /suite/{code}/{id} | Delete test suite.
[**get_suite**](SuitesApi.md#get_suite) | **GET** /suite/{code}/{id} | Get a specific test suite.
[**get_suites**](SuitesApi.md#get_suites) | **GET** /suite/{code} | Get all test suites.
[**update_suite**](SuitesApi.md#update_suite) | **PATCH** /suite/{code}/{id} | Update test suite.

# **create_suite**
> IdResponse create_suite(body, code)

Create a new test suite.

This method is used to create a new test suite through API. 

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
api_instance = qaseio.SuitesApi(qaseio.ApiClient(configuration))
body = qaseio.SuiteCreate() # SuiteCreate | 
code = 'code_example' # str | Code of project, where to search entities.

try:
    # Create a new test suite.
    api_response = api_instance.create_suite(body, code)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SuitesApi->create_suite: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**SuiteCreate**](SuiteCreate.md)|  | 
 **code** | **str**| Code of project, where to search entities. | 

### Return type

[**IdResponse**](IdResponse.md)

### Authorization

[TokenAuth](../README.md#TokenAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_suite**
> IdResponse delete_suite(code, id, body=body)

Delete test suite.

This method completely deletes a test suite with test cases from repository. 

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
api_instance = qaseio.SuitesApi(qaseio.ApiClient(configuration))
code = 'code_example' # str | Code of project, where to search entities.
id = 56 # int | Identifier.
body = qaseio.SuiteDelete() # SuiteDelete |  (optional)

try:
    # Delete test suite.
    api_response = api_instance.delete_suite(code, id, body=body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SuitesApi->delete_suite: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **code** | **str**| Code of project, where to search entities. | 
 **id** | **int**| Identifier. | 
 **body** | [**SuiteDelete**](SuiteDelete.md)|  | [optional] 

### Return type

[**IdResponse**](IdResponse.md)

### Authorization

[TokenAuth](../README.md#TokenAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_suite**
> SuiteResponse get_suite(code, id)

Get a specific test suite.

This method allows to retrieve a specific test suite. 

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
api_instance = qaseio.SuitesApi(qaseio.ApiClient(configuration))
code = 'code_example' # str | Code of project, where to search entities.
id = 56 # int | Identifier.

try:
    # Get a specific test suite.
    api_response = api_instance.get_suite(code, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SuitesApi->get_suite: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **code** | **str**| Code of project, where to search entities. | 
 **id** | **int**| Identifier. | 

### Return type

[**SuiteResponse**](SuiteResponse.md)

### Authorization

[TokenAuth](../README.md#TokenAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_suites**
> SuiteListResponse get_suites(code, filters=filters, limit=limit, offset=offset)

Get all test suites.

This method allows to retrieve all test suites stored in selected project.. 

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
api_instance = qaseio.SuitesApi(qaseio.ApiClient(configuration))
code = 'code_example' # str | Code of project, where to search entities.
filters = qaseio.Filters7() # Filters7 |  (optional)
limit = 10 # int | A number of entities in result set. (optional) (default to 10)
offset = 0 # int | How many entities should be skipped. (optional) (default to 0)

try:
    # Get all test suites.
    api_response = api_instance.get_suites(code, filters=filters, limit=limit, offset=offset)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SuitesApi->get_suites: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **code** | **str**| Code of project, where to search entities. | 
 **filters** | [**Filters7**](.md)|  | [optional] 
 **limit** | **int**| A number of entities in result set. | [optional] [default to 10]
 **offset** | **int**| How many entities should be skipped. | [optional] [default to 0]

### Return type

[**SuiteListResponse**](SuiteListResponse.md)

### Authorization

[TokenAuth](../README.md#TokenAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_suite**
> IdResponse update_suite(body, code, id)

Update test suite.

This method is used to update a test suite through API. 

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
api_instance = qaseio.SuitesApi(qaseio.ApiClient(configuration))
body = qaseio.SuiteCreate() # SuiteCreate | 
code = 'code_example' # str | Code of project, where to search entities.
id = 56 # int | Identifier.

try:
    # Update test suite.
    api_response = api_instance.update_suite(body, code, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SuitesApi->update_suite: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**SuiteCreate**](SuiteCreate.md)|  | 
 **code** | **str**| Code of project, where to search entities. | 
 **id** | **int**| Identifier. | 

### Return type

[**IdResponse**](IdResponse.md)

### Authorization

[TokenAuth](../README.md#TokenAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

