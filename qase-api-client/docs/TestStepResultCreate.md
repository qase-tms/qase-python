# TestStepResultCreate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**position** | **int** |  | [optional] 
**status** | **str** |  | 
**comment** | **str** |  | [optional] 
**attachments** | **List[str]** |  | [optional] 
**action** | **str** |  | [optional] 
**expected_result** | **str** |  | [optional] 
**data** | **str** |  | [optional] 
**steps** | **List[object]** | Nested steps results may be passed here. Use same structure for them. | [optional] 

## Example

```python
from qase.api_client_v1.models.test_step_result_create import TestStepResultCreate

# TODO update the JSON string below
json = "{}"
# create an instance of TestStepResultCreate from a JSON string
test_step_result_create_instance = TestStepResultCreate.from_json(json)
# print the JSON string representation of the object
print(TestStepResultCreate.to_json())

# convert the object into a dict
test_step_result_create_dict = test_step_result_create_instance.to_dict()
# create an instance of TestStepResultCreate from a dict
test_step_result_create_from_dict = TestStepResultCreate.from_dict(test_step_result_create_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


