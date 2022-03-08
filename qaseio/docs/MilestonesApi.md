# qaseio.MilestonesApi

All URIs are relative to *https://api.qase.io/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_milestone**](MilestonesApi.md#create_milestone) | **POST** /milestone/{code} | Create a new milestone.
[**delete_milestone**](MilestonesApi.md#delete_milestone) | **DELETE** /milestone/{code}/{id} | Delete milestone.
[**get_milestone**](MilestonesApi.md#get_milestone) | **GET** /milestone/{code}/{id} | Get a specific milestone.
[**get_milestones**](MilestonesApi.md#get_milestones) | **GET** /milestone/{code} | Get all milestones.
[**update_milestone**](MilestonesApi.md#update_milestone) | **PATCH** /milestone/{code}/{id} | Update milestone.

# **create_milestone**
> IdResponse create_milestone(body, code)

Create a new milestone.

This method allows to create a milestone in selected project. 

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
api_instance = qaseio.MilestonesApi(qaseio.ApiClient(configuration))
body = qaseio.MilestoneCreate() # MilestoneCreate | 
code = 'code_example' # str | Code of project, where to search entities.

try:
    # Create a new milestone.
    api_response = api_instance.create_milestone(body, code)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MilestonesApi->create_milestone: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**MilestoneCreate**](MilestoneCreate.md)|  | 
 **code** | **str**| Code of project, where to search entities. | 

### Return type

[**IdResponse**](IdResponse.md)

### Authorization

[TokenAuth](../README.md#TokenAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_milestone**
> IdResponse delete_milestone(code, id)

Delete milestone.

This method completely deletes a milestone from repository. 

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
api_instance = qaseio.MilestonesApi(qaseio.ApiClient(configuration))
code = 'code_example' # str | Code of project, where to search entities.
id = 56 # int | Identifier.

try:
    # Delete milestone.
    api_response = api_instance.delete_milestone(code, id)
    pprint(api_response)
except ApiException as e:
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

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_milestone**
> MilestoneResponse get_milestone(code, id)

Get a specific milestone.

This method allows to retrieve a specific milestone. 

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
api_instance = qaseio.MilestonesApi(qaseio.ApiClient(configuration))
code = 'code_example' # str | Code of project, where to search entities.
id = 56 # int | Identifier.

try:
    # Get a specific milestone.
    api_response = api_instance.get_milestone(code, id)
    pprint(api_response)
except ApiException as e:
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

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_milestones**
> MilestoneListResponse get_milestones(code, filters=filters, limit=limit, offset=offset)

Get all milestones.

This method allows to retrieve all milestones stored in selected project. 

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
api_instance = qaseio.MilestonesApi(qaseio.ApiClient(configuration))
code = 'code_example' # str | Code of project, where to search entities.
filters = qaseio.Filters3() # Filters3 |  (optional)
limit = 10 # int | A number of entities in result set. (optional) (default to 10)
offset = 0 # int | How many entities should be skipped. (optional) (default to 0)

try:
    # Get all milestones.
    api_response = api_instance.get_milestones(code, filters=filters, limit=limit, offset=offset)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MilestonesApi->get_milestones: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **code** | **str**| Code of project, where to search entities. | 
 **filters** | [**Filters3**](.md)|  | [optional] 
 **limit** | **int**| A number of entities in result set. | [optional] [default to 10]
 **offset** | **int**| How many entities should be skipped. | [optional] [default to 0]

### Return type

[**MilestoneListResponse**](MilestoneListResponse.md)

### Authorization

[TokenAuth](../README.md#TokenAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_milestone**
> IdResponse update_milestone(body, code, id)

Update milestone.

This method updates a milestone. 

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
api_instance = qaseio.MilestonesApi(qaseio.ApiClient(configuration))
body = qaseio.MilestoneUpdate() # MilestoneUpdate | 
code = 'code_example' # str | Code of project, where to search entities.
id = 56 # int | Identifier.

try:
    # Update milestone.
    api_response = api_instance.update_milestone(body, code, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MilestonesApi->update_milestone: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**MilestoneUpdate**](MilestoneUpdate.md)|  | 
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

