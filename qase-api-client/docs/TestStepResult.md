# TestStepResult


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **int** |  | [optional] 
**position** | **int** |  | [optional] 
**attachments** | [**List[Attachment]**](Attachment.md) |  | [optional] 
**steps** | **List[object]** | Nested steps results will be here. The same structure is used for them for them. | [optional] 

## Example

```python
from qase.api_client_v1.models.test_step_result import TestStepResult

# TODO update the JSON string below
json = "{}"
# create an instance of TestStepResult from a JSON string
test_step_result_instance = TestStepResult.from_json(json)
# print the JSON string representation of the object
print(TestStepResult.to_json())

# convert the object into a dict
test_step_result_dict = test_step_result_instance.to_dict()
# create an instance of TestStepResult from a dict
test_step_result_form_dict = test_step_result.from_dict(test_step_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


