# Attachmentupload


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**hash** | **str** |  | [optional] 
**filename** | **str** |  | [optional] 
**mime** | **str** |  | [optional] 
**extension** | **str** |  | [optional] 
**url** | **str** |  | [optional] 
**team** | **str** |  | [optional] 

## Example

```python
from qase.api_client_v1.models.attachmentupload import Attachmentupload

# TODO update the JSON string below
json = "{}"
# create an instance of Attachmentupload from a JSON string
attachmentupload_instance = Attachmentupload.from_json(json)
# print the JSON string representation of the object
print(Attachmentupload.to_json())

# convert the object into a dict
attachmentupload_dict = attachmentupload_instance.to_dict()
# create an instance of Attachmentupload from a dict
attachmentupload_from_dict = Attachmentupload.from_dict(attachmentupload_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


