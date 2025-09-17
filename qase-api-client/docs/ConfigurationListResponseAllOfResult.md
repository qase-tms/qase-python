# ConfigurationListResponseAllOfResult


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**total** | **int** |  | [optional] 
**filtered** | **int** |  | [optional] 
**count** | **int** |  | [optional] 
**entities** | [**List[ConfigurationGroup]**](ConfigurationGroup.md) |  | [optional] 

## Example

```python
from qase.api_client_v1.models.configuration_list_response_all_of_result import ConfigurationListResponseAllOfResult

# TODO update the JSON string below
json = "{}"
# create an instance of ConfigurationListResponseAllOfResult from a JSON string
configuration_list_response_all_of_result_instance = ConfigurationListResponseAllOfResult.from_json(json)
# print the JSON string representation of the object
print(ConfigurationListResponseAllOfResult.to_json())

# convert the object into a dict
configuration_list_response_all_of_result_dict = configuration_list_response_all_of_result_instance.to_dict()
# create an instance of ConfigurationListResponseAllOfResult from a dict
configuration_list_response_all_of_result_from_dict = ConfigurationListResponseAllOfResult.from_dict(configuration_list_response_all_of_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


