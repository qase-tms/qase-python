# Attachment


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**size** | **int** |  | [optional] 
**mime** | **str** |  | [optional] 
**filename** | **str** |  | [optional] 
**url** | **str** |  | [optional] 

## Example

```python
from qase.api_client_v1.models.attachment import Attachment

# TODO update the JSON string below
json = "{}"
# create an instance of Attachment from a JSON string
attachment_instance = Attachment.from_json(json)
# print the JSON string representation of the object
print(Attachment.to_json())

# convert the object into a dict
attachment_dict = attachment_instance.to_dict()
# create an instance of Attachment from a dict
attachment_form_dict = attachment.from_dict(attachment_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


