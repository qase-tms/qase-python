# SharedStepListResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **bool** |  | [optional] 
**result** | [**SharedStepListResponseAllOfResult**](SharedStepListResponseAllOfResult.md) |  | [optional] 

## Example

```python
from src.qase.api_client_v1.models.shared_step_list_response import SharedStepListResponse

# TODO update the JSON string below
json = "{}"
# create an instance of SharedStepListResponse from a JSON string
shared_step_list_response_instance = SharedStepListResponse.from_json(json)
# print the JSON string representation of the object
print(SharedStepListResponse.to_json())

# convert the object into a dict
shared_step_list_response_dict = shared_step_list_response_instance.to_dict()
# create an instance of SharedStepListResponse from a dict
shared_step_list_response_form_dict = shared_step_list_response.from_dict(shared_step_list_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


