# ResultAttachment


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | [optional] 
**file_name** | **str** |  | [optional] 
**mime_type** | **str** |  | [optional] 
**file_path** | **str** |  | [optional] 
**content** | **str** |  | [optional] 
**size** | **int** |  | [optional] 

## Example

```python
from qaseio.models.result_attachment import ResultAttachment

# TODO update the JSON string below
json = "{}"
# create an instance of ResultAttachment from a JSON string
result_attachment_instance = ResultAttachment.from_json(json)
# print the JSON string representation of the object
print ResultAttachment.to_json()

# convert the object into a dict
result_attachment_dict = result_attachment_instance.to_dict()
# create an instance of ResultAttachment from a dict
result_attachment_form_dict = result_attachment.from_dict(result_attachment_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


