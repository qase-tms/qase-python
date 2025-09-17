# CustomFieldUpdate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**title** | **str** |  | 
**value** | [**List[CustomFieldCreateValueInner]**](CustomFieldCreateValueInner.md) |  | [optional] 
**replace_values** | **Dict[str, str]** | Dictionary of old values and their replacemants | [optional] 
**placeholder** | **str** |  | [optional] 
**default_value** | **str** |  | [optional] 
**is_filterable** | **bool** |  | [optional] 
**is_visible** | **bool** |  | [optional] 
**is_required** | **bool** |  | [optional] 
**is_enabled_for_all_projects** | **bool** |  | [optional] 
**projects_codes** | **List[str]** |  | [optional] 

## Example

```python
from qase.api_client_v1.models.custom_field_update import CustomFieldUpdate

# TODO update the JSON string below
json = "{}"
# create an instance of CustomFieldUpdate from a JSON string
custom_field_update_instance = CustomFieldUpdate.from_json(json)
# print the JSON string representation of the object
print(CustomFieldUpdate.to_json())

# convert the object into a dict
custom_field_update_dict = custom_field_update_instance.to_dict()
# create an instance of CustomFieldUpdate from a dict
custom_field_update_from_dict = CustomFieldUpdate.from_dict(custom_field_update_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


