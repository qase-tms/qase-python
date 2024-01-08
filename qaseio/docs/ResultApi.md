# qaseio.ResultApi

All URIs are relative to *https://api.qase.io/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_results_v2**](ResultApi.md#create_results_v2) | **POST** /{project_code}/run/{run_id}/results | (Beta) Bulk create test run result.


# **create_results_v2**
> create_results_v2(project_code, run_id, create_results_request_v2)

(Beta) Bulk create test run result.

This method allows to create a lot of test run result at once.  If there is no free space left in your team account, when attempting to upload an attachment, e.g., through reporters, you will receive an error with code 507 - Insufficient Storage. 

### Example

* Api Key Authentication (TokenAuth):

```python
import time
import os
import qaseio
from qaseio.models.create_results_request_v2 import CreateResultsRequestV2
from qaseio.rest import ApiException
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
configuration.api_key['TokenAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['TokenAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with qaseio.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = qaseio.ResultApi(api_client)
    project_code = 'project_code_example' # str | 
    run_id = 56 # int | 
    create_results_request_v2 = qaseio.CreateResultsRequestV2() # CreateResultsRequestV2 | 

    try:
        # (Beta) Bulk create test run result.
        api_instance.create_results_v2(project_code, run_id, create_results_request_v2)
    except Exception as e:
        print("Exception when calling ResultApi->create_results_v2: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_code** | **str**|  | 
 **run_id** | **int**|  | 
 **create_results_request_v2** | [**CreateResultsRequestV2**](CreateResultsRequestV2.md)|  | 

### Return type

void (empty response body)

### Authorization

[TokenAuth](../README.md#TokenAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**202** | OK |  -  |
**400** | Bad Request |  -  |
**401** | Unauthorized |  -  |
**403** | Forbidden |  -  |
**404** | Not Found |  -  |
**422** | Unprocessable Entity |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

