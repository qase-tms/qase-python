# SharedStep


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**hash** | **str** |  | [optional] 
**title** | **str** |  | [optional] 
**action** | **str** |  | [optional] 
**expected_result** | **str** |  | [optional] 
**steps** | [**List[SharedStepContent]**](SharedStepContent.md) |  | [optional] 
**data** | **str** |  | [optional] 
**cases** | **List[int]** |  | [optional] 
**cases_count** | **int** |  | [optional] 
**created** | **str** | Deprecated, use the &#x60;created_at&#x60; property instead. | [optional] 
**updated** | **str** | Deprecated, use the &#x60;updated_at&#x60; property instead. | [optional] 
**created_at** | **datetime** |  | [optional] 
**updated_at** | **datetime** |  | [optional] 

## Example

```python
from qaseio.models.shared_step import SharedStep

# TODO update the JSON string below
json = "{}"
# create an instance of SharedStep from a JSON string
shared_step_instance = SharedStep.from_json(json)
# print the JSON string representation of the object
print SharedStep.to_json()

# convert the object into a dict
shared_step_dict = shared_step_instance.to_dict()
# create an instance of SharedStep from a dict
shared_step_form_dict = shared_step.from_dict(shared_step_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


