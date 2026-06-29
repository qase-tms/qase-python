# TestStepResult


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **int** | 1 - passed, 2 - failed, 3 - blocked, 5 - skipped, 7 - in_progress | [optional] 
**position** | **int** |  | [optional] 
**comment** | **str** | Comment left for the step. | [optional] 
**start_time** | **int** | Unix timestamp of the step start time. | [optional] 
**end_time** | **int** | Unix timestamp of the step end time. | [optional] 
**duration_ms** | **int** | Step duration in milliseconds. | [optional] 
**attachments** | [**List[Attachment]**](Attachment.md) |  | [optional] 
**steps** | [**List[TestStepResult]**](TestStepResult.md) | Nested steps results will be here. The same structure is used for them. | [optional] 

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
test_step_result_from_dict = TestStepResult.from_dict(test_step_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


