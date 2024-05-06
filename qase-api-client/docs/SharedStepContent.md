# SharedStepContent


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | **str** |  | [optional] 
**hash** | **str** |  | [optional] 
**action** | **str** |  | [optional] 
**expected_result** | **str** |  | [optional] 
**attachments** | [**List[AttachmentHash]**](AttachmentHash.md) |  | [optional] 

## Example

```python
from qase.api_client_v1.models.shared_step_content import SharedStepContent

# TODO update the JSON string below
json = "{}"
# create an instance of SharedStepContent from a JSON string
shared_step_content_instance = SharedStepContent.from_json(json)
# print the JSON string representation of the object
print(SharedStepContent.to_json())

# convert the object into a dict
shared_step_content_dict = shared_step_content_instance.to_dict()
# create an instance of SharedStepContent from a dict
shared_step_content_form_dict = shared_step_content.from_dict(shared_step_content_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


