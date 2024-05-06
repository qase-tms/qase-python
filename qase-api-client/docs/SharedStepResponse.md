# SharedStepResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **bool** |  | [optional] 
**result** | [**SharedStep**](SharedStep.md) |  | [optional] 

## Example

```python
from qase.api_client_v1.models.shared_step_response import SharedStepResponse

# TODO update the JSON string below
json = "{}"
# create an instance of SharedStepResponse from a JSON string
shared_step_response_instance = SharedStepResponse.from_json(json)
# print the JSON string representation of the object
print(SharedStepResponse.to_json())

# convert the object into a dict
shared_step_response_dict = shared_step_response_instance.to_dict()
# create an instance of SharedStepResponse from a dict
shared_step_response_form_dict = shared_step_response.from_dict(shared_step_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


