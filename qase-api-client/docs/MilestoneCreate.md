# MilestoneCreate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**title** | **str** |  | 
**description** | **str** |  | [optional] 
**status** | **str** |  | [optional] 
**due_date** | **int** | unix timestamp | [optional] 

## Example

```python
from src.qase.api_client_v1.models.milestone_create import MilestoneCreate

# TODO update the JSON string below
json = "{}"
# create an instance of MilestoneCreate from a JSON string
milestone_create_instance = MilestoneCreate.from_json(json)
# print the JSON string representation of the object
print(MilestoneCreate.to_json())

# convert the object into a dict
milestone_create_dict = milestone_create_instance.to_dict()
# create an instance of MilestoneCreate from a dict
milestone_create_form_dict = milestone_create.from_dict(milestone_create_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


