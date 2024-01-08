# AttachmentUploadsResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **bool** |  | [optional] 
**result** | [**List[AttachmentGet]**](AttachmentGet.md) |  | [optional] 

## Example

```python
from qaseio.models.attachment_uploads_response import AttachmentUploadsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of AttachmentUploadsResponse from a JSON string
attachment_uploads_response_instance = AttachmentUploadsResponse.from_json(json)
# print the JSON string representation of the object
print AttachmentUploadsResponse.to_json()

# convert the object into a dict
attachment_uploads_response_dict = attachment_uploads_response_instance.to_dict()
# create an instance of AttachmentUploadsResponse from a dict
attachment_uploads_response_form_dict = attachment_uploads_response.from_dict(attachment_uploads_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


