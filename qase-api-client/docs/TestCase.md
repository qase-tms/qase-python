# TestCase


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | [optional] 
**position** | **int** |  | [optional] 
**title** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**preconditions** | **str** |  | [optional] 
**postconditions** | **str** |  | [optional] 
**severity** | **int** |  | [optional] 
**priority** | **int** |  | [optional] 
**type** | **int** |  | [optional] 
**layer** | **int** |  | [optional] 
**is_flaky** | **int** |  | [optional] 
**behavior** | **int** |  | [optional] 
**automation** | **int** |  | [optional] 
**status** | **int** |  | [optional] 
**milestone_id** | **int** |  | [optional] 
**suite_id** | **int** |  | [optional] 
**custom_fields** | [**List[CustomFieldValue]**](CustomFieldValue.md) |  | [optional] 
**attachments** | [**List[Attachment]**](Attachment.md) |  | [optional] 
**steps_type** | **str** |  | [optional] 
**steps** | [**List[TestStep]**](TestStep.md) |  | [optional] 
**params** | [**TestCaseParams**](TestCaseParams.md) |  | [optional] 
**parameters** | [**List[TestCaseParameter]**](TestCaseParameter.md) |  | [optional] 
**tags** | [**List[TagValue]**](TagValue.md) |  | [optional] 
**member_id** | **int** | Deprecated, use &#x60;author_id&#x60; instead. | [optional] 
**author_id** | **int** |  | [optional] 
**created_at** | **datetime** |  | [optional] 
**updated_at** | **datetime** |  | [optional] 
**deleted** | **str** |  | [optional] 
**created** | **str** | Deprecated, use the &#x60;created_at&#x60; property instead. | [optional] 
**updated** | **str** | Deprecated, use the &#x60;updated_at&#x60; property instead. | [optional] 
**external_issues** | [**List[ExternalIssue]**](ExternalIssue.md) |  | [optional] 

## Example

```python
from qase.api_client_v1.models.test_case import TestCase

# TODO update the JSON string below
json = "{}"
# create an instance of TestCase from a JSON string
test_case_instance = TestCase.from_json(json)
# print the JSON string representation of the object
print(TestCase.to_json())

# convert the object into a dict
test_case_dict = test_case_instance.to_dict()
# create an instance of TestCase from a dict
test_case_from_dict = TestCase.from_dict(test_case_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


