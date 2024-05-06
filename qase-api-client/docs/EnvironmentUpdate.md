# EnvironmentUpdate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**title** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**slug** | **str** |  | [optional] 
**host** | **str** |  | [optional] 

## Example

```python
from qase.api_client_v1.models.environment_update import EnvironmentUpdate

# TODO update the JSON string below
json = "{}"
# create an instance of EnvironmentUpdate from a JSON string
environment_update_instance = EnvironmentUpdate.from_json(json)
# print the JSON string representation of the object
print(EnvironmentUpdate.to_json())

# convert the object into a dict
environment_update_dict = environment_update_instance.to_dict()
# create an instance of EnvironmentUpdate from a dict
environment_update_form_dict = environment_update.from_dict(environment_update_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


