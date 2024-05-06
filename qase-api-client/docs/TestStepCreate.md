# TestStepCreate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**action** | **str** |  | [optional] 
**expected_result** | **str** |  | [optional] 
**data** | **str** |  | [optional] 
**position** | **int** |  | [optional] 
**attachments** | **List[str]** | A list of Attachment hashes. | [optional] 
**steps** | **List[object]** | Nested steps may be passed here. Use same structure for them. | [optional] 

## Example

```python
from qase.api_client_v1.models.test_step_create import TestStepCreate

# TODO update the JSON string below
json = "{}"
# create an instance of TestStepCreate from a JSON string
test_step_create_instance = TestStepCreate.from_json(json)
# print the JSON string representation of the object
print(TestStepCreate.to_json())

# convert the object into a dict
test_step_create_dict = test_step_create_instance.to_dict()
# create an instance of TestStepCreate from a dict
test_step_create_form_dict = test_step_create.from_dict(test_step_create_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


