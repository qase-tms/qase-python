# qase.api_client_v1.ConfigurationsApi

All URIs are relative to *https://api.qase.io/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_configuration**](ConfigurationsApi.md#create_configuration) | **POST** /configuration/{code} | Create a new configuration in a particular group.
[**create_configuration_group**](ConfigurationsApi.md#create_configuration_group) | **POST** /configuration/{code}/group | Create a new configuration group.
[**get_configurations**](ConfigurationsApi.md#get_configurations) | **GET** /configuration/{code} | Get all configuration groups with configurations.


# **create_configuration**
> IdResponse create_configuration(code, configuration_create)

Create a new configuration in a particular group.

This method allows to create a configuration in selected project.


### Example

* Api Key Authentication (TokenAuth):

```python
import qase.api_client_v1
from qase.api_client_v1.models.configuration_create import ConfigurationCreate
from qase.api_client_v1.models.id_response import IdResponse
from qase.api_client_v1.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://api.qase.io/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = qase.api_client_v1.Configuration(
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
with qase.api_client_v1.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = qase.api_client_v1.ConfigurationsApi(api_client)
    code = 'code_example' # str | Code of project, where to search entities.
    configuration_create = qase.api_client_v1.ConfigurationCreate() # ConfigurationCreate | 

    try:
        # Create a new configuration in a particular group.
        api_response = api_instance.create_configuration(code, configuration_create)
        print("The response of ConfigurationsApi->create_configuration:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ConfigurationsApi->create_configuration: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **code** | **str**| Code of project, where to search entities. | 
 **configuration_create** | [**ConfigurationCreate**](ConfigurationCreate.md)|  | 

### Return type

[**IdResponse**](IdResponse.md)

### Authorization

[TokenAuth](../README.md#TokenAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A result. |  -  |
**400** | Bad Request. |  -  |
**401** | Unauthorized. |  -  |
**403** | Forbidden. |  -  |
**404** | Not Found. |  -  |
**422** | Unprocessable Entity. |  -  |
**429** | Too Many Requests. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_configuration_group**
> IdResponse create_configuration_group(code, configuration_group_create)

Create a new configuration group.

This method allows to create a configuration group in selected project.


### Example

* Api Key Authentication (TokenAuth):

```python
import qase.api_client_v1
from qase.api_client_v1.models.configuration_group_create import ConfigurationGroupCreate
from qase.api_client_v1.models.id_response import IdResponse
from qase.api_client_v1.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://api.qase.io/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = qase.api_client_v1.Configuration(
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
with qase.api_client_v1.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = qase.api_client_v1.ConfigurationsApi(api_client)
    code = 'code_example' # str | Code of project, where to search entities.
    configuration_group_create = qase.api_client_v1.ConfigurationGroupCreate() # ConfigurationGroupCreate | 

    try:
        # Create a new configuration group.
        api_response = api_instance.create_configuration_group(code, configuration_group_create)
        print("The response of ConfigurationsApi->create_configuration_group:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ConfigurationsApi->create_configuration_group: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **code** | **str**| Code of project, where to search entities. | 
 **configuration_group_create** | [**ConfigurationGroupCreate**](ConfigurationGroupCreate.md)|  | 

### Return type

[**IdResponse**](IdResponse.md)

### Authorization

[TokenAuth](../README.md#TokenAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A result. |  -  |
**400** | Bad Request. |  -  |
**401** | Unauthorized. |  -  |
**403** | Forbidden. |  -  |
**404** | Not Found. |  -  |
**422** | Unprocessable Entity. |  -  |
**429** | Too Many Requests. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_configurations**
> ConfigurationListResponse get_configurations(code)

Get all configuration groups with configurations.

This method allows to retrieve all configurations groups with configurations


### Example

* Api Key Authentication (TokenAuth):

```python
import qase.api_client_v1
from qase.api_client_v1.models.configuration_list_response import ConfigurationListResponse
from qase.api_client_v1.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://api.qase.io/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = qase.api_client_v1.Configuration(
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
with qase.api_client_v1.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = qase.api_client_v1.ConfigurationsApi(api_client)
    code = 'code_example' # str | Code of project, where to search entities.

    try:
        # Get all configuration groups with configurations.
        api_response = api_instance.get_configurations(code)
        print("The response of ConfigurationsApi->get_configurations:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ConfigurationsApi->get_configurations: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **code** | **str**| Code of project, where to search entities. | 

### Return type

[**ConfigurationListResponse**](ConfigurationListResponse.md)

### Authorization

[TokenAuth](../README.md#TokenAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A list of all configurations. |  -  |
**400** | Bad Request. |  -  |
**401** | Unauthorized. |  -  |
**403** | Forbidden. |  -  |
**404** | Not Found. |  -  |
**429** | Too Many Requests. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

