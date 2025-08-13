# TestCasebulkCasesInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**description** | **str** |  | [optional] 
**preconditions** | **str** |  | [optional] 
**postconditions** | **str** |  | [optional] 
**title** | **str** |  | 
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
**parameters** | [**List[TestCaseParametercreate]**](TestCaseParametercreate.md) |  | [optional] 
**custom_field** | **Dict[str, str]** | A map of custom fields values (id &#x3D;&gt; value) | [optional] 
**created_at** | **str** |  | [optional] 
**updated_at** | **str** |  | [optional] 
**id** | **int** |  | [optional] 

## Example

```python
from qase.api_client_v1.models.test_casebulk_cases_inner import TestCasebulkCasesInner

# TODO update the JSON string below
json = "{}"
# create an instance of TestCasebulkCasesInner from a JSON string
test_casebulk_cases_inner_instance = TestCasebulkCasesInner.from_json(json)
# print the JSON string representation of the object
print(TestCasebulkCasesInner.to_json())

# convert the object into a dict
test_casebulk_cases_inner_dict = test_casebulk_cases_inner_instance.to_dict()
# create an instance of TestCasebulkCasesInner from a dict
test_casebulk_cases_inner_form_dict = test_casebulk_cases_inner.from_dict(test_casebulk_cases_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


