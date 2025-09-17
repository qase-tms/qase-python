# DefectCreate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**title** | **str** |  | 
**actual_result** | **str** |  | 
**severity** | **int** |  | 
**milestone_id** | **int** |  | [optional] 
**attachments** | **List[str]** |  | [optional] 
**custom_field** | **Dict[str, str]** | A map of custom fields values (id &#x3D;&gt; value) | [optional] 
**tags** | **List[str]** |  | [optional] 

## Example

```python
from qase.api_client_v1.models.defect_create import DefectCreate

# TODO update the JSON string below
json = "{}"
# create an instance of DefectCreate from a JSON string
defect_create_instance = DefectCreate.from_json(json)
# print the JSON string representation of the object
print(DefectCreate.to_json())

# convert the object into a dict
defect_create_dict = defect_create_instance.to_dict()
# create an instance of DefectCreate from a dict
defect_create_from_dict = DefectCreate.from_dict(defect_create_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


