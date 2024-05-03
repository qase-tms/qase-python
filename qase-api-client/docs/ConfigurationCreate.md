# ConfigurationCreate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**title** | **str** |  | 
**group_id** | **int** |  | 

## Example

```python
from src.qase.api_client_v1.models.configuration_create import ConfigurationCreate

# TODO update the JSON string below
json = "{}"
# create an instance of ConfigurationCreate from a JSON string
configuration_create_instance = ConfigurationCreate.from_json(json)
# print the JSON string representation of the object
print(ConfigurationCreate.to_json())

# convert the object into a dict
configuration_create_dict = configuration_create_instance.to_dict()
# create an instance of ConfigurationCreate from a dict
configuration_create_form_dict = configuration_create.from_dict(configuration_create_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


