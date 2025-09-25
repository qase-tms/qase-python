# Configuration


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | [optional] 
**title** | **str** |  | [optional] 

## Example

```python
from qase.api_client_v1.models.configuration_model import ConfigurationModel

# TODO update the JSON string below
json = "{}"
# create an instance of ConfigurationModel from a JSON string
configuration_instance = ConfigurationModel.from_json(json)
# print the JSON string representation of the object
print(ConfigurationModel.to_json())

# convert the object into a dict
configuration_dict = configuration_instance.to_dict()
# create an instance of ConfigurationModel from a dict
configuration_from_dict = ConfigurationModel.from_dict(configuration_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


