# TestCaseCreate


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
**author_id** | **int** |  | [optional] 
**suite_id** | **int** |  | [optional] 
**milestone_id** | **int** |  | [optional] 
**automation** | **int** |  | [optional] 
**status** | **int** |  | [optional] 
**attachments** | **List[str]** | A list of Attachment hashes. | [optional] 
**steps** | [**List[TestStepCreate]**](TestStepCreate.md) |  | [optional] 
**tags** | **List[str]** |  | [optional] 
**params** | **Dict[str, List[str]]** |  | [optional] 
**custom_field** | **Dict[str, str]** | A map of custom fields values (id &#x3D;&gt; value) | [optional] 
**created_at** | **str** |  | [optional] 
**updated_at** | **str** |  | [optional] 

## Example

```python
from src.qase.api_client_v1.models.test_case_create import TestCaseCreate

# TODO update the JSON string below
json = "{}"
# create an instance of TestCaseCreate from a JSON string
test_case_create_instance = TestCaseCreate.from_json(json)
# print the JSON string representation of the object
print(TestCaseCreate.to_json())

# convert the object into a dict
test_case_create_dict = test_case_create_instance.to_dict()
# create an instance of TestCaseCreate from a dict
test_case_create_form_dict = test_case_create.from_dict(test_case_create_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


