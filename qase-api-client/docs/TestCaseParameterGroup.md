# TestCaseParameterGroup


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**shared_id** | **str** |  | [optional] 
**type** | **str** |  | 
**items** | **object** |  | 

## Example

```python
from qase.api_client_v1.models.test_case_parameter_group import TestCaseParameterGroup

# TODO update the JSON string below
json = "{}"
# create an instance of TestCaseParameterGroup from a JSON string
test_case_parameter_group_instance = TestCaseParameterGroup.from_json(json)
# print the JSON string representation of the object
print(TestCaseParameterGroup.to_json())

# convert the object into a dict
test_case_parameter_group_dict = test_case_parameter_group_instance.to_dict()
# create an instance of TestCaseParameterGroup from a dict
test_case_parameter_group_form_dict = test_case_parameter_group.from_dict(test_case_parameter_group_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


