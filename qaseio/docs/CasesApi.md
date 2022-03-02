# qaseio.CasesApi

All URIs are relative to *https://api.qase.io/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_case**](CasesApi.md#create_case) | **POST** /case/{code} | Create a new test case.
[**delete_case**](CasesApi.md#delete_case) | **DELETE** /case/{code}/{id} | Delete test case.
[**get_case**](CasesApi.md#get_case) | **GET** /case/{code}/{id} | Get a specific test case.
[**get_cases**](CasesApi.md#get_cases) | **GET** /case/{code} | Get all test cases.
[**update_case**](CasesApi.md#update_case) | **PATCH** /case/{code}/{id} | Update test case.

# **create_case**
> IdResponse create_case(body, code)

Create a new test case.

This method allows to create a new test case in selected project. 

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
api_instance = qaseio.CasesApi(qaseio.ApiClient(configuration))
body = qaseio.TestCaseCreate() # TestCaseCreate | 
code = 'code_example' # str | Code of project, where to search entities.

try:
    # Create a new test case.
    api_response = api_instance.create_case(body, code)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CasesApi->create_case: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**TestCaseCreate**](TestCaseCreate.md)|  | 
 **code** | **str**| Code of project, where to search entities. | 

### Return type

[**IdResponse**](IdResponse.md)

### Authorization

[TokenAuth](../README.md#TokenAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_case**
> IdResponse delete_case(code, id)

Delete test case.

This method completely deletes a test case from repository. 

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
api_instance = qaseio.CasesApi(qaseio.ApiClient(configuration))
code = 'code_example' # str | Code of project, where to search entities.
id = 56 # int | Identifier.

try:
    # Delete test case.
    api_response = api_instance.delete_case(code, id)
    pprint(api_response)
except ApiException as e:
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

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_case**
> TestCaseResponse get_case(code, id)

Get a specific test case.

This method allows to retrieve a specific test case. 

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
api_instance = qaseio.CasesApi(qaseio.ApiClient(configuration))
code = 'code_example' # str | Code of project, where to search entities.
id = 56 # int | Identifier.

try:
    # Get a specific test case.
    api_response = api_instance.get_case(code, id)
    pprint(api_response)
except ApiException as e:
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

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_cases**
> TestCaseListResponse get_cases(code, filters=filters, limit=limit, offset=offset)

Get all test cases.

This method allows to retrieve all test cases stored in selected project. 

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
api_instance = qaseio.CasesApi(qaseio.ApiClient(configuration))
code = 'code_example' # str | Code of project, where to search entities.
filters = qaseio.Filters() # Filters |  (optional)
limit = 10 # int | A number of entities in result set. (optional) (default to 10)
offset = 0 # int | How many entities should be skipped. (optional) (default to 0)

try:
    # Get all test cases.
    api_response = api_instance.get_cases(code, filters=filters, limit=limit, offset=offset)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CasesApi->get_cases: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **code** | **str**| Code of project, where to search entities. | 
 **filters** | [**Filters**](.md)|  | [optional] 
 **limit** | **int**| A number of entities in result set. | [optional] [default to 10]
 **offset** | **int**| How many entities should be skipped. | [optional] [default to 0]

### Return type

[**TestCaseListResponse**](TestCaseListResponse.md)

### Authorization

[TokenAuth](../README.md#TokenAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_case**
> IdResponse update_case(body, code, id)

Update test case.

This method updates a test case. 

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
api_instance = qaseio.CasesApi(qaseio.ApiClient(configuration))
body = qaseio.TestCaseUpdate() # TestCaseUpdate | 
code = 'code_example' # str | Code of project, where to search entities.
id = 56 # int | Identifier.

try:
    # Update test case.
    api_response = api_instance.update_case(body, code, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CasesApi->update_case: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**TestCaseUpdate**](TestCaseUpdate.md)|  | 
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

