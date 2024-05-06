# AttachmentHash


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**size** | **int** |  | [optional] 
**mime** | **str** |  | [optional] 
**filename** | **str** |  | [optional] 
**url** | **str** |  | [optional] 
**hash** | **str** |  | [optional] 

## Example

```python
from qase.api_client_v1.models.attachment_hash import AttachmentHash

# TODO update the JSON string below
json = "{}"
# create an instance of AttachmentHash from a JSON string
attachment_hash_instance = AttachmentHash.from_json(json)
# print the JSON string representation of the object
print(AttachmentHash.to_json())

# convert the object into a dict
attachment_hash_dict = attachment_hash_instance.to_dict()
# create an instance of AttachmentHash from a dict
attachment_hash_form_dict = attachment_hash.from_dict(attachment_hash_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


