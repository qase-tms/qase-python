# qaseio.SharedStepsApi

All URIs are relative to *https://api.qase.io/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_shared_step**](SharedStepsApi.md#create_shared_step) | **POST** /shared_step/{code} | Create a new shared step.
[**delete_shared_step**](SharedStepsApi.md#delete_shared_step) | **DELETE** /shared_step/{code}/{hash} | Delete shared step.
[**get_shared_step**](SharedStepsApi.md#get_shared_step) | **GET** /shared_step/{code}/{hash} | Get a specific shared step.
[**get_shared_steps**](SharedStepsApi.md#get_shared_steps) | **GET** /shared_step/{code} | Get all shared steps.
[**update_shared_step**](SharedStepsApi.md#update_shared_step) | **PATCH** /shared_step/{code}/{hash} | Update shared step.

# **create_shared_step**
> HashResponse create_shared_step(body, code)

Create a new shared step.

This method allows to create a shared step in selected project. 

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
api_instance = qaseio.SharedStepsApi(qaseio.ApiClient(configuration))
body = qaseio.SharedStepCreate() # SharedStepCreate | 
code = 'code_example' # str | Code of project, where to search entities.

try:
    # Create a new shared step.
    api_response = api_instance.create_shared_step(body, code)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SharedStepsApi->create_shared_step: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**SharedStepCreate**](SharedStepCreate.md)|  | 
 **code** | **str**| Code of project, where to search entities. | 

### Return type

[**HashResponse**](HashResponse.md)

### Authorization

[TokenAuth](../README.md#TokenAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_shared_step**
> HashResponse delete_shared_step(code, hash)

Delete shared step.

This method completely deletes a shared step from repository. 

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
api_instance = qaseio.SharedStepsApi(qaseio.ApiClient(configuration))
code = 'code_example' # str | Code of project, where to search entities.
hash = 'hash_example' # str | Hash.

try:
    # Delete shared step.
    api_response = api_instance.delete_shared_step(code, hash)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SharedStepsApi->delete_shared_step: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **code** | **str**| Code of project, where to search entities. | 
 **hash** | **str**| Hash. | 

### Return type

[**HashResponse**](HashResponse.md)

### Authorization

[TokenAuth](../README.md#TokenAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_shared_step**
> SharedStepResponse get_shared_step(code, hash)

Get a specific shared step.

This method allows to retrieve a specific shared step. 

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
api_instance = qaseio.SharedStepsApi(qaseio.ApiClient(configuration))
code = 'code_example' # str | Code of project, where to search entities.
hash = 'hash_example' # str | Hash.

try:
    # Get a specific shared step.
    api_response = api_instance.get_shared_step(code, hash)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SharedStepsApi->get_shared_step: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **code** | **str**| Code of project, where to search entities. | 
 **hash** | **str**| Hash. | 

### Return type

[**SharedStepResponse**](SharedStepResponse.md)

### Authorization

[TokenAuth](../README.md#TokenAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_shared_steps**
> SharedStepListResponse get_shared_steps(code, filters=filters, limit=limit, offset=offset)

Get all shared steps.

This method allows to retrieve all shared steps stored in selected project. 

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
api_instance = qaseio.SharedStepsApi(qaseio.ApiClient(configuration))
code = 'code_example' # str | Code of project, where to search entities.
filters = qaseio.Filters6() # Filters6 |  (optional)
limit = 10 # int | A number of entities in result set. (optional) (default to 10)
offset = 0 # int | How many entities should be skipped. (optional) (default to 0)

try:
    # Get all shared steps.
    api_response = api_instance.get_shared_steps(code, filters=filters, limit=limit, offset=offset)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SharedStepsApi->get_shared_steps: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **code** | **str**| Code of project, where to search entities. | 
 **filters** | [**Filters6**](.md)|  | [optional] 
 **limit** | **int**| A number of entities in result set. | [optional] [default to 10]
 **offset** | **int**| How many entities should be skipped. | [optional] [default to 0]

### Return type

[**SharedStepListResponse**](SharedStepListResponse.md)

### Authorization

[TokenAuth](../README.md#TokenAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_shared_step**
> HashResponse update_shared_step(body, code, hash)

Update shared step.

This method updates a shared step. 

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
api_instance = qaseio.SharedStepsApi(qaseio.ApiClient(configuration))
body = qaseio.SharedStepUpdate() # SharedStepUpdate | 
code = 'code_example' # str | Code of project, where to search entities.
hash = 'hash_example' # str | Hash.

try:
    # Update shared step.
    api_response = api_instance.update_shared_step(body, code, hash)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SharedStepsApi->update_shared_step: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**SharedStepUpdate**](SharedStepUpdate.md)|  | 
 **code** | **str**| Code of project, where to search entities. | 
 **hash** | **str**| Hash. | 

### Return type

[**HashResponse**](HashResponse.md)

### Authorization

[TokenAuth](../README.md#TokenAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

