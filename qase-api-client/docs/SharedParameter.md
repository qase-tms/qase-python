# SharedParameter


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **UUID** |  | 
**title** | **str** |  | 
**type** | **str** |  | 
**project_codes** | **List[str]** |  | 
**is_enabled_for_all_projects** | **bool** |  | 
**parameters** | [**SharedParameterParameter**](SharedParameterParameter.md) |  | 

## Example

```python
from qase.api_client_v1.models.shared_parameter import SharedParameter

# TODO update the JSON string below
json = "{}"
# create an instance of SharedParameter from a JSON string
shared_parameter_instance = SharedParameter.from_json(json)
# print the JSON string representation of the object
print(SharedParameter.to_json())

# convert the object into a dict
shared_parameter_dict = shared_parameter_instance.to_dict()
# create an instance of SharedParameter from a dict
shared_parameter_from_dict = SharedParameter.from_dict(shared_parameter_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


