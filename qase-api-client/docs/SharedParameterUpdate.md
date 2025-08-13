# SharedParameterUpdate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**title** | **str** |  | [optional] 
**project_codes** | **List[str]** | List of project codes to associate with this shared parameter | [optional] 
**is_enabled_for_all_projects** | **bool** |  | [optional] 
**parameters** | [**SharedParameterParameter**](SharedParameterParameter.md) |  | [optional] 

## Example

```python
from qase.api_client_v1.models.shared_parameter_update import SharedParameterUpdate

# TODO update the JSON string below
json = "{}"
# create an instance of SharedParameterUpdate from a JSON string
shared_parameter_update_instance = SharedParameterUpdate.from_json(json)
# print the JSON string representation of the object
print(SharedParameterUpdate.to_json())

# convert the object into a dict
shared_parameter_update_dict = shared_parameter_update_instance.to_dict()
# create an instance of SharedParameterUpdate from a dict
shared_parameter_update_form_dict = shared_parameter_update.from_dict(shared_parameter_update_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


