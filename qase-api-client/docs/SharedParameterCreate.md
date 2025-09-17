# SharedParameterCreate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**title** | **str** |  | 
**type** | **str** |  | 
**project_codes** | **List[str]** | List of project codes to associate with this shared parameter | [optional] 
**is_enabled_for_all_projects** | **bool** |  | 
**parameters** | [**SharedParameterParameter**](SharedParameterParameter.md) |  | 

## Example

```python
from qase.api_client_v1.models.shared_parameter_create import SharedParameterCreate

# TODO update the JSON string below
json = "{}"
# create an instance of SharedParameterCreate from a JSON string
shared_parameter_create_instance = SharedParameterCreate.from_json(json)
# print the JSON string representation of the object
print(SharedParameterCreate.to_json())

# convert the object into a dict
shared_parameter_create_dict = shared_parameter_create_instance.to_dict()
# create an instance of SharedParameterCreate from a dict
shared_parameter_create_from_dict = SharedParameterCreate.from_dict(shared_parameter_create_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


