# SystemField


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**title** | **str** |  | [optional] 
**slug** | **str** |  | [optional] 
**default_value** | **str** |  | [optional] 
**is_required** | **bool** |  | [optional] 
**entity** | **int** |  | [optional] 
**type** | **int** |  | [optional] 
**options** | [**List[SystemFieldOption]**](SystemFieldOption.md) |  | [optional] 

## Example

```python
from qase.api_client_v1.models.system_field import SystemField

# TODO update the JSON string below
json = "{}"
# create an instance of SystemField from a JSON string
system_field_instance = SystemField.from_json(json)
# print the JSON string representation of the object
print(SystemField.to_json())

# convert the object into a dict
system_field_dict = system_field_instance.to_dict()
# create an instance of SystemField from a dict
system_field_from_dict = SystemField.from_dict(system_field_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


