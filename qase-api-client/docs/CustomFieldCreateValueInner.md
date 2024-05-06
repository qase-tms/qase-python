# CustomFieldCreateValueInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | [optional] 
**title** | **str** |  | [optional] 

## Example

```python
from qase.api_client_v1.models.custom_field_create_value_inner import CustomFieldCreateValueInner

# TODO update the JSON string below
json = "{}"
# create an instance of CustomFieldCreateValueInner from a JSON string
custom_field_create_value_inner_instance = CustomFieldCreateValueInner.from_json(json)
# print the JSON string representation of the object
print(CustomFieldCreateValueInner.to_json())

# convert the object into a dict
custom_field_create_value_inner_dict = custom_field_create_value_inner_instance.to_dict()
# create an instance of CustomFieldCreateValueInner from a dict
custom_field_create_value_inner_form_dict = custom_field_create_value_inner.from_dict(
    custom_field_create_value_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


