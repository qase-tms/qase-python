# MilestoneUpdate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**title** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**status** | **str** |  | [optional] 

## Example

```python
from qaseio.models.milestone_update import MilestoneUpdate

# TODO update the JSON string below
json = "{}"
# create an instance of MilestoneUpdate from a JSON string
milestone_update_instance = MilestoneUpdate.from_json(json)
# print the JSON string representation of the object
print MilestoneUpdate.to_json()

# convert the object into a dict
milestone_update_dict = milestone_update_instance.to_dict()
# create an instance of MilestoneUpdate from a dict
milestone_update_form_dict = milestone_update.from_dict(milestone_update_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


