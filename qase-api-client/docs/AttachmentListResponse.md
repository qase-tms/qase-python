# AttachmentListResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **bool** |  | [optional] 
**result** | [**AttachmentListResponseAllOfResult**](AttachmentListResponseAllOfResult.md) |  | [optional] 

## Example

```python
from src.qase.api_client_v1.models.attachment_list_response import AttachmentListResponse

# TODO update the JSON string below
json = "{}"
# create an instance of AttachmentListResponse from a JSON string
attachment_list_response_instance = AttachmentListResponse.from_json(json)
# print the JSON string representation of the object
print(AttachmentListResponse.to_json())

# convert the object into a dict
attachment_list_response_dict = attachment_list_response_instance.to_dict()
# create an instance of AttachmentListResponse from a dict
attachment_list_response_form_dict = attachment_list_response.from_dict(attachment_list_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


