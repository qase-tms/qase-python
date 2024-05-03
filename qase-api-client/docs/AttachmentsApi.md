# src.qase.apiv1.AttachmentsApi

All URIs are relative to *https://api.qase.io/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**delete_attachment**](AttachmentsApi.md#delete_attachment) | **DELETE** /attachment/{hash} | Remove attachment by Hash
[**get_attachment**](AttachmentsApi.md#get_attachment) | **GET** /attachment/{hash} | Get attachment by Hash
[**get_attachments**](AttachmentsApi.md#get_attachments) | **GET** /attachment | Get all attachments
[**upload_attachment**](AttachmentsApi.md#upload_attachment) | **POST** /attachment/{code} | Upload attachment


# **delete_attachment**
> HashResponse delete_attachment(hash)

Remove attachment by Hash

This method allows to remove attachment by Hash. 

### Example

* Api Key Authentication (TokenAuth):

```python
import src.qase.api_client_v1
from src.qase.api_client_v1.models.hash_response import HashResponse
from src.qase.api_client_v1.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://api.qase.io/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = src.qase.apiv1.Configuration(
    host="https://api.qase.io/v1"
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
with src.qase.apiv1.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = src.qase.apiv1.AttachmentsApi(api_client)
    hash = 'hash_example'  # str | Hash.

    try:
        # Remove attachment by Hash
        api_response = api_instance.delete_attachment(hash)
        print("The response of AttachmentsApi->delete_attachment:\n")
        pprint(api_response)
    except Exception as e:
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

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A result. |  -  |
**400** | Bad Request. |  -  |
**401** | Unauthorized. |  -  |
**403** | Forbidden. |  -  |
**404** | Not Found. |  -  |
**429** | Too Many Requests. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_attachment**
> AttachmentResponse get_attachment(hash)

Get attachment by Hash

This method allows to retrieve attachment by Hash. 

### Example

* Api Key Authentication (TokenAuth):

```python
import src.qase.api_client_v1
from src.qase.api_client_v1.models.attachment_response import AttachmentResponse
from src.qase.api_client_v1.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://api.qase.io/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = src.qase.apiv1.Configuration(
    host="https://api.qase.io/v1"
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
with src.qase.apiv1.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = src.qase.apiv1.AttachmentsApi(api_client)
    hash = 'hash_example'  # str | Hash.

    try:
        # Get attachment by Hash
        api_response = api_instance.get_attachment(hash)
        print("The response of AttachmentsApi->get_attachment:\n")
        pprint(api_response)
    except Exception as e:
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

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Single attachment. |  -  |
**400** | Bad Request. |  -  |
**401** | Unauthorized. |  -  |
**403** | Forbidden. |  -  |
**404** | Not Found. |  -  |
**429** | Too Many Requests. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_attachments**
> AttachmentListResponse get_attachments(limit=limit, offset=offset)

Get all attachments

This method allows to retrieve attachments. 

### Example

* Api Key Authentication (TokenAuth):

```python
import src.qase.api_client_v1
from src.qase.api_client_v1.models.attachment_list_response import AttachmentListResponse
from src.qase.api_client_v1.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://api.qase.io/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = src.qase.apiv1.Configuration(
    host="https://api.qase.io/v1"
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
with src.qase.apiv1.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = src.qase.apiv1.AttachmentsApi(api_client)
    limit = 10  # int | A number of entities in result set. (optional) (default to 10)
    offset = 0  # int | How many entities should be skipped. (optional) (default to 0)

    try:
        # Get all attachments
        api_response = api_instance.get_attachments(limit=limit, offset=offset)
        print("The response of AttachmentsApi->get_attachments:\n")
        pprint(api_response)
    except Exception as e:
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

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A list of all attachments. |  -  |
**400** | Bad Request. |  -  |
**401** | Unauthorized. |  -  |
**403** | Forbidden. |  -  |
**404** | Not Found. |  -  |
**413** | Payload Too Large. |  -  |
**429** | Too Many Requests. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **upload_attachment**
> AttachmentUploadsResponse upload_attachment(code, file=file)

Upload attachment

This method allows to upload attachment to Qase. Max upload size: * Up to 32 Mb per file * Up to 128 Mb per single request * Up to 20 files per single request  If there is no free space left in your team account, you will receive an error with code 507 - Insufficient Storage. 

### Example

* Api Key Authentication (TokenAuth):

```python
import src.qase.api_client_v1
from src.qase.api_client_v1.models.attachment_uploads_response import AttachmentUploadsResponse
from src.qase.api_client_v1.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://api.qase.io/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = src.qase.apiv1.Configuration(
    host="https://api.qase.io/v1"
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
with src.qase.apiv1.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = src.qase.apiv1.AttachmentsApi(api_client)
    code = 'code_example'  # str | Code of project, where to search entities.
    file = None  # List[bytearray] |  (optional)

    try:
        # Upload attachment
        api_response = api_instance.upload_attachment(code, file=file)
        print("The response of AttachmentsApi->upload_attachment:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AttachmentsApi->upload_attachment: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **code** | **str**| Code of project, where to search entities. | 
 **file** | **List[bytearray]**|  | [optional] 

### Return type

[**AttachmentUploadsResponse**](AttachmentUploadsResponse.md)

### Authorization

[TokenAuth](../README.md#TokenAuth)

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | An attachments. |  -  |
**400** | Bad Request. |  -  |
**401** | Unauthorized. |  -  |
**403** | Forbidden. |  -  |
**404** | Not Found. |  -  |
**413** | Payload Too Large. |  -  |
**429** | Too Many Requests. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

