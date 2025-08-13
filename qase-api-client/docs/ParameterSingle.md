# ParameterSingle

Single parameter

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**title** | **str** |  | 
**values** | **List[str]** |  | 

## Example

```python
from qase.api_client_v1.models.parameter_single import ParameterSingle

# TODO update the JSON string below
json = "{}"
# create an instance of ParameterSingle from a JSON string
parameter_single_instance = ParameterSingle.from_json(json)
# print the JSON string representation of the object
print(ParameterSingle.to_json())

# convert the object into a dict
parameter_single_dict = parameter_single_instance.to_dict()
# create an instance of ParameterSingle from a dict
parameter_single_form_dict = parameter_single.from_dict(parameter_single_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


