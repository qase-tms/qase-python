# SystemFieldOption


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | [optional] 
**title** | **str** |  | [optional] 
**slug** | **str** |  | [optional] 
**color** | **str** |  | [optional] 
**icon** | **str** |  | [optional] 
**is_default** | **bool** |  | [optional] 
**read_only** | **bool** |  | [optional] 

## Example

```python
from qaseio.models.system_field_option import SystemFieldOption

# TODO update the JSON string below
json = "{}"
# create an instance of SystemFieldOption from a JSON string
system_field_option_instance = SystemFieldOption.from_json(json)
# print the JSON string representation of the object
print SystemFieldOption.to_json()

# convert the object into a dict
system_field_option_dict = system_field_option_instance.to_dict()
# create an instance of SystemFieldOption from a dict
system_field_option_form_dict = system_field_option.from_dict(system_field_option_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


