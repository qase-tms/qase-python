# AttachmentGet


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**hash** | **str** |  | [optional] 
**file** | **str** |  | [optional] 
**mime** | **str** |  | [optional] 
**size** | **int** |  | [optional] 
**extension** | **str** |  | [optional] 
**full_path** | **str** |  | [optional] 

## Example

```python
from qaseio.models.attachment_get import AttachmentGet

# TODO update the JSON string below
json = "{}"
# create an instance of AttachmentGet from a JSON string
attachment_get_instance = AttachmentGet.from_json(json)
# print the JSON string representation of the object
print AttachmentGet.to_json()

# convert the object into a dict
attachment_get_dict = attachment_get_instance.to_dict()
# create an instance of AttachmentGet from a dict
attachment_get_form_dict = attachment_get.from_dict(attachment_get_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


