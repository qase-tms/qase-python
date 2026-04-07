# TestStep


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**hash** | **str** |  | [optional] 
**shared_step_hash** | **str** |  | [optional] 
**shared_step_nested_hash** | **str** |  | [optional] 
**position** | **int** |  | [optional] 
**action** | **str** |  | [optional] 
**expected_result** | **str** |  | [optional] 
**data** | **str** |  | [optional] 
**attachments** | [**List[Attachment]**](Attachment.md) |  | [optional] 
**steps** | **List[object]** | Nested steps will be here. The same structure is used for them. | [optional] 

## Example

```python
from qase.api_client_v1.models.test_step import TestStep

# TODO update the JSON string below
json = "{}"
# create an instance of TestStep from a JSON string
test_step_instance = TestStep.from_json(json)
# print the JSON string representation of the object
print(TestStep.to_json())

# convert the object into a dict
test_step_dict = test_step_instance.to_dict()
# create an instance of TestStep from a dict
test_step_from_dict = TestStep.from_dict(test_step_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


