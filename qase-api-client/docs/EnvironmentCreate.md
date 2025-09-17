# EnvironmentCreate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**title** | **str** |  | 
**description** | **str** |  | [optional] 
**slug** | **str** |  | 
**host** | **str** |  | [optional] 

## Example

```python
from qase.api_client_v1.models.environment_create import EnvironmentCreate

# TODO update the JSON string below
json = "{}"
# create an instance of EnvironmentCreate from a JSON string
environment_create_instance = EnvironmentCreate.from_json(json)
# print the JSON string representation of the object
print(EnvironmentCreate.to_json())

# convert the object into a dict
environment_create_dict = environment_create_instance.to_dict()
# create an instance of EnvironmentCreate from a dict
environment_create_from_dict = EnvironmentCreate.from_dict(environment_create_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


