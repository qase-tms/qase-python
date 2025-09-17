# ConfigurationGroup


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | [optional] 
**title** | **str** |  | [optional] 
**configurations** | [**List[Configuration]**](Configuration.md) |  | [optional] 

## Example

```python
from qase.api_client_v1.models.configuration_group import ConfigurationGroup

# TODO update the JSON string below
json = "{}"
# create an instance of ConfigurationGroup from a JSON string
configuration_group_instance = ConfigurationGroup.from_json(json)
# print the JSON string representation of the object
print(ConfigurationGroup.to_json())

# convert the object into a dict
configuration_group_dict = configuration_group_instance.to_dict()
# create an instance of ConfigurationGroup from a dict
configuration_group_from_dict = ConfigurationGroup.from_dict(configuration_group_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


