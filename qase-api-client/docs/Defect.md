# Defect


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | [optional] 
**title** | **str** |  | [optional] 
**actual_result** | **str** |  | [optional] 
**severity** | **str** |  | [optional] 
**status** | **str** |  | [optional] 
**milestone_id** | **int** |  | [optional] 
**custom_fields** | [**List[CustomFieldValue]**](CustomFieldValue.md) |  | [optional] 
**attachments** | [**List[Attachment]**](Attachment.md) |  | [optional] 
**resolved_at** | **datetime** |  | [optional] 
**member_id** | **int** | Deprecated, use &#x60;author_id&#x60; instead. | [optional] 
**author_id** | **int** |  | [optional] 
**external_data** | **str** |  | [optional] 
**tags** | [**List[TagValue]**](TagValue.md) |  | [optional] 
**created_at** | **datetime** |  | [optional] 
**updated_at** | **datetime** |  | [optional] 
**created** | **str** | Deprecated, use the &#x60;created_at&#x60; property instead. | [optional] 
**updated** | **str** | Deprecated, use the &#x60;updated_at&#x60; property instead. | [optional] 

## Example

```python
from qase.api_client_v1.models.defect import Defect

# TODO update the JSON string below
json = "{}"
# create an instance of Defect from a JSON string
defect_instance = Defect.from_json(json)
# print the JSON string representation of the object
print(Defect.to_json())

# convert the object into a dict
defect_dict = defect_instance.to_dict()
# create an instance of Defect from a dict
defect_form_dict = defect.from_dict(defect_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


