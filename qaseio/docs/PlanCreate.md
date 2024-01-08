# PlanCreate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**title** | **str** |  | 
**description** | **str** |  | [optional] 
**cases** | **List[int]** |  | 

## Example

```python
from qaseio.models.plan_create import PlanCreate

# TODO update the JSON string below
json = "{}"
# create an instance of PlanCreate from a JSON string
plan_create_instance = PlanCreate.from_json(json)
# print the JSON string representation of the object
print PlanCreate.to_json()

# convert the object into a dict
plan_create_dict = plan_create_instance.to_dict()
# create an instance of PlanCreate from a dict
plan_create_form_dict = plan_create.from_dict(plan_create_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


