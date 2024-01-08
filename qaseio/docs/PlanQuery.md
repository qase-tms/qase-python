# PlanQuery


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | [optional] 
**title** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**cases_count** | **int** |  | [optional] 
**created_at** | **datetime** |  | [optional] 
**updated_at** | **datetime** |  | [optional] 

## Example

```python
from qaseio.models.plan_query import PlanQuery

# TODO update the JSON string below
json = "{}"
# create an instance of PlanQuery from a JSON string
plan_query_instance = PlanQuery.from_json(json)
# print the JSON string representation of the object
print PlanQuery.to_json()

# convert the object into a dict
plan_query_dict = plan_query_instance.to_dict()
# create an instance of PlanQuery from a dict
plan_query_form_dict = plan_query.from_dict(plan_query_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


