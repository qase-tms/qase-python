# QqlTestCase


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | [optional] 
**test_case_id** | **int** |  | 
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
**params** | [**QqlTestCaseParams**](QqlTestCaseParams.md) |  | [optional] 
**tags** | [**List[TagValue]**](TagValue.md) |  | [optional] 
**member_id** | **int** | Deprecated, use &#x60;author_id&#x60; instead. | [optional] 
**author_id** | **int** |  | [optional] 
**created_at** | **datetime** |  | [optional] 
**updated_at** | **datetime** |  | [optional] 
**updated_by** | **int** | Author ID of the last update. | [optional] 

## Example

```python
from qase.api_client_v1.models.qql_test_case import QqlTestCase

# TODO update the JSON string below
json = "{}"
# create an instance of QqlTestCase from a JSON string
qql_test_case_instance = QqlTestCase.from_json(json)
# print the JSON string representation of the object
print(QqlTestCase.to_json())

# convert the object into a dict
qql_test_case_dict = qql_test_case_instance.to_dict()
# create an instance of QqlTestCase from a dict
qql_test_case_form_dict = qql_test_case.from_dict(qql_test_case_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


