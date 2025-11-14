# CustomField


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | [optional] 
**title** | **str** |  | [optional] 
**entity** | **str** |  | [optional] 
**type** | **str** |  | [optional] 
**placeholder** | **str** |  | [optional] 
**default_value** | **str** |  | [optional] 
**value** | [**List[CustomFieldOption]**](CustomFieldOption.md) |  | [optional] 
**is_required** | **bool** |  | [optional] 
**is_visible** | **bool** |  | [optional] 
**is_filterable** | **bool** |  | [optional] 
**is_enabled_for_all_projects** | **bool** |  | [optional] 
**created_at** | **datetime** |  | [optional] 
**updated_at** | **datetime** |  | [optional] 
**projects_codes** | **List[str]** |  | [optional] 

## Example

```python
from qase.api_client_v2.models.custom_field import CustomField

# TODO update the JSON string below
json = "{}"
# create an instance of CustomField from a JSON string
custom_field_instance = CustomField.from_json(json)
# print the JSON string representation of the object
print(CustomField.to_json())

# convert the object into a dict
custom_field_dict = custom_field_instance.to_dict()
# create an instance of CustomField from a dict
custom_field_from_dict = CustomField.from_dict(custom_field_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


