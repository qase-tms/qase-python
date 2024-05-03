# SharedStepUpdate


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
from src.qase.api_client_v1.models.shared_step_update import SharedStepUpdate

# TODO update the JSON string below
json = "{}"
# create an instance of SharedStepUpdate from a JSON string
shared_step_update_instance = SharedStepUpdate.from_json(json)
# print the JSON string representation of the object
print(SharedStepUpdate.to_json())

# convert the object into a dict
shared_step_update_dict = shared_step_update_instance.to_dict()
# create an instance of SharedStepUpdate from a dict
shared_step_update_form_dict = shared_step_update.from_dict(shared_step_update_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


