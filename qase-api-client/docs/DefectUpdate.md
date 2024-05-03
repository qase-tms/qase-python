# DefectUpdate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**title** | **str** |  | [optional] 
**actual_result** | **str** |  | [optional] 
**severity** | **int** |  | [optional] 
**milestone_id** | **int** |  | [optional] 
**attachments** | **List[str]** |  | [optional] 
**custom_field** | **Dict[str, str]** | A map of custom fields values (id &#x3D;&gt; value) | [optional] 
**tags** | **List[str]** |  | [optional] 

## Example

```python
from src.qase.api_client_v1.models.defect_update import DefectUpdate

# TODO update the JSON string below
json = "{}"
# create an instance of DefectUpdate from a JSON string
defect_update_instance = DefectUpdate.from_json(json)
# print the JSON string representation of the object
print(DefectUpdate.to_json())

# convert the object into a dict
defect_update_dict = defect_update_instance.to_dict()
# create an instance of DefectUpdate from a dict
defect_update_form_dict = defect_update.from_dict(defect_update_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


