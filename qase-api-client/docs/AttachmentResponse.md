# AttachmentResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **bool** |  | [optional] 
**result** | [**AttachmentGet**](AttachmentGet.md) |  | [optional] 

## Example

```python
from qase.api_client_v1.models.attachment_response import AttachmentResponse

# TODO update the JSON string below
json = "{}"
# create an instance of AttachmentResponse from a JSON string
attachment_response_instance = AttachmentResponse.from_json(json)
# print the JSON string representation of the object
print(AttachmentResponse.to_json())

# convert the object into a dict
attachment_response_dict = attachment_response_instance.to_dict()
# create an instance of AttachmentResponse from a dict
attachment_response_form_dict = attachment_response.from_dict(attachment_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


