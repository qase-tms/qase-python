# TestCaseUpdate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**description** | **str** |  | [optional] 
**preconditions** | **str** |  | [optional] 
**postconditions** | **str** |  | [optional] 
**title** | **str** |  | [optional] 
**severity** | **int** |  | [optional] 
**priority** | **int** |  | [optional] 
**behavior** | **int** |  | [optional] 
**type** | **int** |  | [optional] 
**layer** | **int** |  | [optional] 
**is_flaky** | **int** |  | [optional] 
**suite_id** | **int** |  | [optional] 
**milestone_id** | **int** |  | [optional] 
**automation** | **int** |  | [optional] 
**status** | **int** |  | [optional] 
**attachments** | **List[str]** | A list of Attachment hashes. | [optional] 
**steps** | [**List[TestStepCreate]**](TestStepCreate.md) |  | [optional] 
**tags** | **List[str]** |  | [optional] 
**params** | **Dict[str, List[str]]** | Deprecated, use &#x60;parameters&#x60; instead. | [optional] 
**parameters** | [**List[TestCaseParameterCreate]**](TestCaseParameterCreate.md) |  | [optional] 
**custom_field** | **Dict[str, str]** | A map of custom fields values (id &#x3D;&gt; value) | [optional] 

## Example

```python
from qase.api_client_v1.models.test_case_update import TestCaseUpdate

# TODO update the JSON string below
json = "{}"
# create an instance of TestCaseUpdate from a JSON string
test_case_update_instance = TestCaseUpdate.from_json(json)
# print the JSON string representation of the object
print(TestCaseUpdate.to_json())

# convert the object into a dict
test_case_update_dict = test_case_update_instance.to_dict()
# create an instance of TestCaseUpdate from a dict
test_case_update_from_dict = TestCaseUpdate.from_dict(test_case_update_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


