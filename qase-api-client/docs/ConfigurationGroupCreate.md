# ConfigurationGroupCreate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**title** | **str** |  | 

## Example

```python
from qase.api_client_v1.models.configuration_group_create import ConfigurationGroupCreate

# TODO update the JSON string below
json = "{}"
# create an instance of ConfigurationGroupCreate from a JSON string
configuration_group_create_instance = ConfigurationGroupCreate.from_json(json)
# print the JSON string representation of the object
print(ConfigurationGroupCreate.to_json())

# convert the object into a dict
configuration_group_create_dict = configuration_group_create_instance.to_dict()
# create an instance of ConfigurationGroupCreate from a dict
configuration_group_create_form_dict = configuration_group_create.from_dict(configuration_group_create_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


