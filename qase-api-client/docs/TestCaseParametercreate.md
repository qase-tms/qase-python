# TestCaseParameterCreate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**shared_id** | **str** |  | 
**title** | **str** |  | 
**values** | **List[str]** |  | 
**items** | [**List[ParameterSingle]**](ParameterSingle.md) |  | 

## Example

```python
from qase.api_client_v1.models.test_case_parameter_create import TestCaseParameterCreate

# TODO update the JSON string below
json = "{}"
# create an instance of TestCaseParameterCreate from a JSON string
test_case_parameter_create_instance = TestCaseParameterCreate.from_json(json)
# print the JSON string representation of the object
print(TestCaseParameterCreate.to_json())

# convert the object into a dict
test_case_parameter_create_dict = test_case_parameter_create_instance.to_dict()
# create an instance of TestCaseParameterCreate from a dict
test_case_parameter_create_from_dict = TestCaseParameterCreate.from_dict(test_case_parameter_create_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


