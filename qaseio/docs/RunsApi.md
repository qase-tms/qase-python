# qaseio.RunsApi

All URIs are relative to *https://api.qase.io/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**complete_run**](RunsApi.md#complete_run) | **POST** /run/{code}/{id}/complete | Complete a specific run.
[**create_run**](RunsApi.md#create_run) | **POST** /run/{code} | Create a new run.
[**delete_run**](RunsApi.md#delete_run) | **DELETE** /run/{code}/{id} | Delete run.
[**get_run**](RunsApi.md#get_run) | **GET** /run/{code}/{id} | Get a specific run.
[**get_runs**](RunsApi.md#get_runs) | **GET** /run/{code} | Get all runs.
[**update_run_publicity**](RunsApi.md#update_run_publicity) | **PATCH** /run/{code}/{id}/public | Update publicity of a specific run.

# **complete_run**
> Response complete_run(code, id)

Complete a specific run.

This method allows to complete a specific run. 

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
api_instance = qaseio.RunsApi(qaseio.ApiClient(configuration))
code = 'code_example' # str | Code of project, where to search entities.
id = 56 # int | Identifier.

try:
    # Complete a specific run.
    api_response = api_instance.complete_run(code, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RunsApi->complete_run: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **code** | **str**| Code of project, where to search entities. | 
 **id** | **int**| Identifier. | 

### Return type

[**Response**](Response.md)

### Authorization

[TokenAuth](../README.md#TokenAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_run**
> IdResponse create_run(body, code)

Create a new run.

This method allows to create a run in selected project. 

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
api_instance = qaseio.RunsApi(qaseio.ApiClient(configuration))
body = qaseio.RunCreate() # RunCreate | 
code = 'code_example' # str | Code of project, where to search entities.

try:
    # Create a new run.
    api_response = api_instance.create_run(body, code)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RunsApi->create_run: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**RunCreate**](RunCreate.md)|  | 
 **code** | **str**| Code of project, where to search entities. | 

### Return type

[**IdResponse**](IdResponse.md)

### Authorization

[TokenAuth](../README.md#TokenAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_run**
> IdResponse delete_run(code, id)

Delete run.

This method completely deletes a run from repository. 

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
api_instance = qaseio.RunsApi(qaseio.ApiClient(configuration))
code = 'code_example' # str | Code of project, where to search entities.
id = 56 # int | Identifier.

try:
    # Delete run.
    api_response = api_instance.delete_run(code, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RunsApi->delete_run: %s\n" % e)
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

# **get_run**
> RunResponse get_run(code, id, include=include)

Get a specific run.

This method allows to retrieve a specific run. 

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
api_instance = qaseio.RunsApi(qaseio.ApiClient(configuration))
code = 'code_example' # str | Code of project, where to search entities.
id = 56 # int | Identifier.
include = 'include_example' # str | Add this param to include a list of test cases into response. Possible value: cases  (optional)

try:
    # Get a specific run.
    api_response = api_instance.get_run(code, id, include=include)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RunsApi->get_run: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **code** | **str**| Code of project, where to search entities. | 
 **id** | **int**| Identifier. | 
 **include** | **str**| Add this param to include a list of test cases into response. Possible value: cases  | [optional] 

### Return type

[**RunResponse**](RunResponse.md)

### Authorization

[TokenAuth](../README.md#TokenAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_runs**
> RunListResponse get_runs(code, filters=filters, limit=limit, offset=offset, include=include)

Get all runs.

This method allows to retrieve all runs stored in selected project. 

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
api_instance = qaseio.RunsApi(qaseio.ApiClient(configuration))
code = 'code_example' # str | Code of project, where to search entities.
filters = qaseio.Filters5() # Filters5 |  (optional)
limit = 10 # int | A number of entities in result set. (optional) (default to 10)
offset = 0 # int | How many entities should be skipped. (optional) (default to 0)
include = 'include_example' # str | Add this param to include a list of test cases into response. Possible value: cases  (optional)

try:
    # Get all runs.
    api_response = api_instance.get_runs(code, filters=filters, limit=limit, offset=offset, include=include)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RunsApi->get_runs: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **code** | **str**| Code of project, where to search entities. | 
 **filters** | [**Filters5**](.md)|  | [optional] 
 **limit** | **int**| A number of entities in result set. | [optional] [default to 10]
 **offset** | **int**| How many entities should be skipped. | [optional] [default to 0]
 **include** | **str**| Add this param to include a list of test cases into response. Possible value: cases  | [optional] 

### Return type

[**RunListResponse**](RunListResponse.md)

### Authorization

[TokenAuth](../README.md#TokenAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_run_publicity**
> RunPublicResponse update_run_publicity(body, code, id)

Update publicity of a specific run.

This method allows to update a publicity of specific run. 

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
api_instance = qaseio.RunsApi(qaseio.ApiClient(configuration))
body = qaseio.RunPublic() # RunPublic | 
code = 'code_example' # str | Code of project, where to search entities.
id = 56 # int | Identifier.

try:
    # Update publicity of a specific run.
    api_response = api_instance.update_run_publicity(body, code, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RunsApi->update_run_publicity: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**RunPublic**](RunPublic.md)|  | 
 **code** | **str**| Code of project, where to search entities. | 
 **id** | **int**| Identifier. | 

### Return type

[**RunPublicResponse**](RunPublicResponse.md)

### Authorization

[TokenAuth](../README.md#TokenAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

