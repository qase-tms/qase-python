# AttachmentListResponseAllOfResult


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**total** | **int** |  | [optional] 
**filtered** | **int** |  | [optional] 
**count** | **int** |  | [optional] 
**entities** | [**List[AttachmentGet]**](AttachmentGet.md) |  | [optional] 

## Example

```python
from qaseio.models.attachment_list_response_all_of_result import AttachmentListResponseAllOfResult

# TODO update the JSON string below
json = "{}"
# create an instance of AttachmentListResponseAllOfResult from a JSON string
attachment_list_response_all_of_result_instance = AttachmentListResponseAllOfResult.from_json(json)
# print the JSON string representation of the object
print AttachmentListResponseAllOfResult.to_json()

# convert the object into a dict
attachment_list_response_all_of_result_dict = attachment_list_response_all_of_result_instance.to_dict()
# create an instance of AttachmentListResponseAllOfResult from a dict
attachment_list_response_all_of_result_form_dict = attachment_list_response_all_of_result.from_dict(attachment_list_response_all_of_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


