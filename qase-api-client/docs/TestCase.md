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
**automation** | **int** | Deprecated, use &#x60;isManual&#x60; and &#x60;isToBeAutomated&#x60; instead. Encodes the test case automation state as a single integer: &#x60;0&#x60; &#x3D; manual, &#x60;1&#x60; &#x3D; manual planned to be automated, &#x60;2&#x60; &#x3D; automated. | [optional] 
**is_manual** | **int** | &#x60;1&#x60; if the case is manual, &#x60;0&#x60; if it is automated. Combined with &#x60;isToBeAutomated&#x60;, replaces the deprecated &#x60;automation&#x60; field. | [optional] 
**is_to_be_automated** | **int** | &#x60;1&#x60; if a manual case is planned to be automated, &#x60;0&#x60; otherwise. Only meaningful when &#x60;isManual &#x3D; 1&#x60;; ignored when &#x60;isManual &#x3D; 0&#x60;. | [optional] 
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


