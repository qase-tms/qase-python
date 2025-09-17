# TestCaseParameterSingle


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**shared_id** | **str** |  | [optional] 
**type** | **str** |  | 
**item** | [**ParameterSingle**](ParameterSingle.md) |  | 

## Example

```python
from qase.api_client_v1.models.test_case_parameter_single import TestCaseParameterSingle

# TODO update the JSON string below
json = "{}"
# create an instance of TestCaseParameterSingle from a JSON string
test_case_parameter_single_instance = TestCaseParameterSingle.from_json(json)
# print the JSON string representation of the object
print(TestCaseParameterSingle.to_json())

# convert the object into a dict
test_case_parameter_single_dict = test_case_parameter_single_instance.to_dict()
# create an instance of TestCaseParameterSingle from a dict
test_case_parameter_single_from_dict = TestCaseParameterSingle.from_dict(test_case_parameter_single_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


