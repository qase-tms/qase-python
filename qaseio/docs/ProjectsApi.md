# qaseio.ProjectsApi

All URIs are relative to *https://api.qase.io/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_project**](ProjectsApi.md#create_project) | **POST** /project | Create new project.
[**delete_project**](ProjectsApi.md#delete_project) | **DELETE** /project/{code} | Delete Project by code.
[**get_project**](ProjectsApi.md#get_project) | **GET** /project/{code} | Get Project by code.
[**get_projects**](ProjectsApi.md#get_projects) | **GET** /project | Get All Projects.
[**grant_access_to_project**](ProjectsApi.md#grant_access_to_project) | **POST** /project/{code}/access | Grant access to project by code.
[**revoke_access_to_project**](ProjectsApi.md#revoke_access_to_project) | **DELETE** /project/{code}/access | Revoke access to project by code.

# **create_project**
> ProjectCodeResponse create_project(body)

Create new project.

This method is used to create a new project through API. 

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
api_instance = qaseio.ProjectsApi(qaseio.ApiClient(configuration))
body = qaseio.ProjectCreate() # ProjectCreate | 

try:
    # Create new project.
    api_response = api_instance.create_project(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProjectsApi->create_project: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ProjectCreate**](ProjectCreate.md)|  | 

### Return type

[**ProjectCodeResponse**](ProjectCodeResponse.md)

### Authorization

[TokenAuth](../README.md#TokenAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_project**
> Response delete_project(code)

Delete Project by code.

This method allows to delete a specific project. 

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
api_instance = qaseio.ProjectsApi(qaseio.ApiClient(configuration))
code = 'code_example' # str | Code of project, where to search entities.

try:
    # Delete Project by code.
    api_response = api_instance.delete_project(code)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProjectsApi->delete_project: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **code** | **str**| Code of project, where to search entities. | 

### Return type

[**Response**](Response.md)

### Authorization

[TokenAuth](../README.md#TokenAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_project**
> ProjectResponse get_project(code)

Get Project by code.

This method allows to retrieve a specific project. 

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
api_instance = qaseio.ProjectsApi(qaseio.ApiClient(configuration))
code = 'code_example' # str | Code of project, where to search entities.

try:
    # Get Project by code.
    api_response = api_instance.get_project(code)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProjectsApi->get_project: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **code** | **str**| Code of project, where to search entities. | 

### Return type

[**ProjectResponse**](ProjectResponse.md)

### Authorization

[TokenAuth](../README.md#TokenAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_projects**
> ProjectListResponse get_projects(limit=limit, offset=offset)

Get All Projects.

This method allows to retrieve all projects available for your account. You can limit and offset params to paginate. 

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
api_instance = qaseio.ProjectsApi(qaseio.ApiClient(configuration))
limit = 10 # int | A number of entities in result set. (optional) (default to 10)
offset = 0 # int | How many entities should be skipped. (optional) (default to 0)

try:
    # Get All Projects.
    api_response = api_instance.get_projects(limit=limit, offset=offset)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProjectsApi->get_projects: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **int**| A number of entities in result set. | [optional] [default to 10]
 **offset** | **int**| How many entities should be skipped. | [optional] [default to 0]

### Return type

[**ProjectListResponse**](ProjectListResponse.md)

### Authorization

[TokenAuth](../README.md#TokenAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **grant_access_to_project**
> Response grant_access_to_project(body, code)

Grant access to project by code.

This method allows to grant access to a specific project. 

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
api_instance = qaseio.ProjectsApi(qaseio.ApiClient(configuration))
body = qaseio.ProjectAccess() # ProjectAccess | 
code = 'code_example' # str | Code of project, where to search entities.

try:
    # Grant access to project by code.
    api_response = api_instance.grant_access_to_project(body, code)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProjectsApi->grant_access_to_project: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ProjectAccess**](ProjectAccess.md)|  | 
 **code** | **str**| Code of project, where to search entities. | 

### Return type

[**Response**](Response.md)

### Authorization

[TokenAuth](../README.md#TokenAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **revoke_access_to_project**
> Response revoke_access_to_project(body, code)

Revoke access to project by code.

This method allows to revoke access to a specific project. 

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
api_instance = qaseio.ProjectsApi(qaseio.ApiClient(configuration))
body = qaseio.ProjectAccess() # ProjectAccess | 
code = 'code_example' # str | Code of project, where to search entities.

try:
    # Revoke access to project by code.
    api_response = api_instance.revoke_access_to_project(body, code)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProjectsApi->revoke_access_to_project: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ProjectAccess**](ProjectAccess.md)|  | 
 **code** | **str**| Code of project, where to search entities. | 

### Return type

[**Response**](Response.md)

### Authorization

[TokenAuth](../README.md#TokenAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

