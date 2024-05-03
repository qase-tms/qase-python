# SharedStepContentCreate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**hash** | **str** |  | [optional] 
**action** | **str** |  | 
**expected_result** | **str** |  | [optional] 
**data** | **str** |  | [optional] 
**attachments** | **List[str]** | A list of Attachment hashes. | [optional] 

## Example

```python
from src.qase.api_client_v1.models.shared_step_content_create import SharedStepContentCreate

# TODO update the JSON string below
json = "{}"
# create an instance of SharedStepContentCreate from a JSON string
shared_step_content_create_instance = SharedStepContentCreate.from_json(json)
# print the JSON string representation of the object
print(SharedStepContentCreate.to_json())

# convert the object into a dict
shared_step_content_create_dict = shared_step_content_create_instance.to_dict()
# create an instance of SharedStepContentCreate from a dict
shared_step_content_create_form_dict = shared_step_content_create.from_dict(shared_step_content_create_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


