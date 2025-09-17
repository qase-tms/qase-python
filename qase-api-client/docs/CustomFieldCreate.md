# CustomFieldCreate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**title** | **str** |  | 
**value** | [**List[CustomFieldCreateValueInner]**](CustomFieldCreateValueInner.md) | Required if type one of: 3 - selectbox; 5 - radio; 6 - multiselect;  | [optional] 
**entity** | **int** | Possible values: 0 - case; 1 - run; 2 - defect;  | 
**type** | **int** | Possible values: 0 - number; 1 - string; 2 - text; 3 - selectbox; 4 - checkbox; 5 - radio; 6 - multiselect; 7 - url; 8 - user; 9 - datetime;  | 
**placeholder** | **str** |  | [optional] 
**default_value** | **str** |  | [optional] 
**is_filterable** | **bool** |  | [optional] 
**is_visible** | **bool** |  | [optional] 
**is_required** | **bool** |  | [optional] 
**is_enabled_for_all_projects** | **bool** |  | [optional] 
**projects_codes** | **List[str]** |  | [optional] 

## Example

```python
from qase.api_client_v1.models.custom_field_create import CustomFieldCreate

# TODO update the JSON string below
json = "{}"
# create an instance of CustomFieldCreate from a JSON string
custom_field_create_instance = CustomFieldCreate.from_json(json)
# print the JSON string representation of the object
print(CustomFieldCreate.to_json())

# convert the object into a dict
custom_field_create_dict = custom_field_create_instance.to_dict()
# create an instance of CustomFieldCreate from a dict
custom_field_create_from_dict = CustomFieldCreate.from_dict(custom_field_create_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


