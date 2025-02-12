# QqlDefect


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | [optional] 
**defect_id** | **int** |  | 
**title** | **str** |  | [optional] 
**actual_result** | **str** |  | [optional] 
**severity** | **str** |  | [optional] 
**status** | **str** |  | [optional] 
**milestone_id** | **int** |  | [optional] 
**custom_fields** | [**List[CustomFieldValue]**](CustomFieldValue.md) |  | [optional] 
**attachments** | [**List[Attachment]**](Attachment.md) |  | [optional] 
**resolved** | **datetime** |  | [optional] 
**member_id** | **int** | Deprecated, use &#x60;author_id&#x60; instead. | [optional] 
**author_id** | **int** |  | [optional] 
**external_data** | **str** |  | [optional] 
**tags** | [**List[TagValue]**](TagValue.md) |  | [optional] 
**created_at** | **datetime** |  | [optional] 
**updated_at** | **datetime** |  | [optional] 

## Example

```python
from qase.api_client_v1.models.qql_defect import QqlDefect

# TODO update the JSON string below
json = "{}"
# create an instance of QqlDefect from a JSON string
qql_defect_instance = QqlDefect.from_json(json)
# print the JSON string representation of the object
print(QqlDefect.to_json())

# convert the object into a dict
qql_defect_dict = qql_defect_instance.to_dict()
# create an instance of QqlDefect from a dict
qql_defect_form_dict = qql_defect.from_dict(qql_defect_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


