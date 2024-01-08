# SharedStepCreate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**title** | **str** |  | 
**action** | **str** | Deprecated, use the &#x60;steps&#x60; property instead. | [optional] 
**expected_result** | **str** | Deprecated, use the &#x60;steps&#x60; property instead. | [optional] 
**data** | **str** | Deprecated, use the &#x60;steps&#x60; property instead. | [optional] 
**steps** | [**List[SharedStepContentCreate]**](SharedStepContentCreate.md) |  | [optional] 

## Example

```python
from qaseio.models.shared_step_create import SharedStepCreate

# TODO update the JSON string below
json = "{}"
# create an instance of SharedStepCreate from a JSON string
shared_step_create_instance = SharedStepCreate.from_json(json)
# print the JSON string representation of the object
print SharedStepCreate.to_json()

# convert the object into a dict
shared_step_create_dict = shared_step_create_instance.to_dict()
# create an instance of SharedStepCreate from a dict
shared_step_create_form_dict = shared_step_create.from_dict(shared_step_create_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


