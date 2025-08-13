# TestCaseParameterBase


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**shared_id** | **str** |  | [optional] 
**type** | **str** |  | 
**items** | [**List[ParameterSingle]**](ParameterSingle.md) |  | 

## Example

```python
from qase.api_client_v1.models.test_case_parameter_base import TestCaseParameterBase

# TODO update the JSON string below
json = "{}"
# create an instance of TestCaseParameterBase from a JSON string
test_case_parameter_base_instance = TestCaseParameterBase.from_json(json)
# print the JSON string representation of the object
print(TestCaseParameterBase.to_json())

# convert the object into a dict
test_case_parameter_base_dict = test_case_parameter_base_instance.to_dict()
# create an instance of TestCaseParameterBase from a dict
test_case_parameter_base_form_dict = test_case_parameter_base.from_dict(test_case_parameter_base_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


