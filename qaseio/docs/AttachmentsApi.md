# qaseio.AttachmentsApi

All URIs are relative to *https://api.qase.io/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**delete_attachment**](AttachmentsApi.md#delete_attachment) | **DELETE** /attachment/{hash} | Remove attachment by Hash.
[**get_attachment**](AttachmentsApi.md#get_attachment) | **GET** /attachment/{hash} | Get attachment by Hash.
[**get_attachments**](AttachmentsApi.md#get_attachments) | **GET** /attachment | Get all attachments.
[**upload_attachment**](AttachmentsApi.md#upload_attachment) | **POST** /attachment/{code} | Upload attachment.

# **delete_attachment**
> HashResponse delete_attachment(hash)

Remove attachment by Hash.

This method allows to remove attachment by Hash. 

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
api_instance = qaseio.AttachmentsApi(qaseio.ApiClient(configuration))
hash = 'hash_example' # str | Hash.

try:
    # Remove attachment by Hash.
    api_response = api_instance.delete_attachment(hash)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AttachmentsApi->delete_attachment: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **hash** | **str**| Hash. | 

### Return type

[**HashResponse**](HashResponse.md)

### Authorization

[TokenAuth](../README.md#TokenAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_attachment**
> AttachmentResponse get_attachment(hash)

Get attachment by Hash.

This method allows to retrieve attachment by Hash. 

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
api_instance = qaseio.AttachmentsApi(qaseio.ApiClient(configuration))
hash = 'hash_example' # str | Hash.

try:
    # Get attachment by Hash.
    api_response = api_instance.get_attachment(hash)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AttachmentsApi->get_attachment: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **hash** | **str**| Hash. | 

### Return type

[**AttachmentResponse**](AttachmentResponse.md)

### Authorization

[TokenAuth](../README.md#TokenAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_attachments**
> AttachmentListResponse get_attachments(limit=limit, offset=offset)

Get all attachments.

This method allows to retrieve attachments. 

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
api_instance = qaseio.AttachmentsApi(qaseio.ApiClient(configuration))
limit = 10 # int | A number of entities in result set. (optional) (default to 10)
offset = 0 # int | How many entities should be skipped. (optional) (default to 0)

try:
    # Get all attachments.
    api_response = api_instance.get_attachments(limit=limit, offset=offset)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AttachmentsApi->get_attachments: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **int**| A number of entities in result set. | [optional] [default to 10]
 **offset** | **int**| How many entities should be skipped. | [optional] [default to 0]

### Return type

[**AttachmentListResponse**](AttachmentListResponse.md)

### Authorization

[TokenAuth](../README.md#TokenAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **upload_attachment**
> AttachmentUploadsResponse upload_attachment(code, file=file)

Upload attachment.

This method allows to upload attachment to Qase. Max upload size: * Up to 32 Mb per file * Up to 128 Mb per single request * Up to 20 files per single request  If there is no free space left in your team account, you will receive an error with code 507 - Insufficient Storage. 

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
api_instance = qaseio.AttachmentsApi(qaseio.ApiClient(configuration))
code = 'code_example' # str | Code of project, where to search entities.
file = ['file_example'] # list[str] |  (optional)

try:
    # Upload attachment.
    api_response = api_instance.upload_attachment(code, file=file)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AttachmentsApi->upload_attachment: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **code** | **str**| Code of project, where to search entities. | 
 **file** | [**list[str]**](str.md)|  | [optional] 

### Return type

[**AttachmentUploadsResponse**](AttachmentUploadsResponse.md)

### Authorization

[TokenAuth](../README.md#TokenAuth)

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

