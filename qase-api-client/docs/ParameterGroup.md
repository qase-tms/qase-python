# ParameterGroup

Group parameter

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**items** | [**List[ParameterSingle]**](ParameterSingle.md) |  | 

## Example

```python
from qase.api_client_v1.models.parameter_group import ParameterGroup

# TODO update the JSON string below
json = "{}"
# create an instance of ParameterGroup from a JSON string
parameter_group_instance = ParameterGroup.from_json(json)
# print the JSON string representation of the object
print(ParameterGroup.to_json())

# convert the object into a dict
parameter_group_dict = parameter_group_instance.to_dict()
# create an instance of ParameterGroup from a dict
parameter_group_form_dict = parameter_group.from_dict(parameter_group_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


