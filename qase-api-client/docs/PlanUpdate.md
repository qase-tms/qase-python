# PlanUpdate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**title** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**cases** | **List[int]** |  | [optional] 

## Example

```python
from qase.api_client_v1.models.plan_update import PlanUpdate

# TODO update the JSON string below
json = "{}"
# create an instance of PlanUpdate from a JSON string
plan_update_instance = PlanUpdate.from_json(json)
# print the JSON string representation of the object
print(PlanUpdate.to_json())

# convert the object into a dict
plan_update_dict = plan_update_instance.to_dict()
# create an instance of PlanUpdate from a dict
plan_update_from_dict = PlanUpdate.from_dict(plan_update_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


