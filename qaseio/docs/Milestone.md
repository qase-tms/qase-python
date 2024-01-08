# Milestone


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | [optional] 
**title** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**status** | **str** |  | [optional] 
**due_date** | **datetime** |  | [optional] 
**created** | **str** | Deprecated, use the &#x60;created_at&#x60; property instead. | [optional] 
**updated** | **str** | Deprecated, use the &#x60;updated_at&#x60; property instead. | [optional] 
**created_at** | **datetime** |  | [optional] 
**updated_at** | **datetime** |  | [optional] 

## Example

```python
from qaseio.models.milestone import Milestone

# TODO update the JSON string below
json = "{}"
# create an instance of Milestone from a JSON string
milestone_instance = Milestone.from_json(json)
# print the JSON string representation of the object
print Milestone.to_json()

# convert the object into a dict
milestone_dict = milestone_instance.to_dict()
# create an instance of Milestone from a dict
milestone_form_dict = milestone.from_dict(milestone_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


