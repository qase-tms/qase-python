# ConfigurationListResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **bool** |  | [optional] 
**result** | [**ConfigurationListResponseAllOfResult**](ConfigurationListResponseAllOfResult.md) |  | [optional] 

## Example

```python
from qase.api_client_v1.models.configuration_list_response import ConfigurationListResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ConfigurationListResponse from a JSON string
configuration_list_response_instance = ConfigurationListResponse.from_json(json)
# print the JSON string representation of the object
print(ConfigurationListResponse.to_json())

# convert the object into a dict
configuration_list_response_dict = configuration_list_response_instance.to_dict()
# create an instance of ConfigurationListResponse from a dict
configuration_list_response_from_dict = ConfigurationListResponse.from_dict(configuration_list_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


