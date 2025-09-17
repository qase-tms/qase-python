# PlanQuery


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | [optional] 
**plan_id** | **int** |  | 
**title** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**cases_count** | **int** |  | [optional] 
**created_at** | **datetime** |  | [optional] 
**updated_at** | **datetime** |  | [optional] 

## Example

```python
from qase.api_client_v1.models.plan_query import PlanQuery

# TODO update the JSON string below
json = "{}"
# create an instance of PlanQuery from a JSON string
plan_query_instance = PlanQuery.from_json(json)
# print the JSON string representation of the object
print(PlanQuery.to_json())

# convert the object into a dict
plan_query_dict = plan_query_instance.to_dict()
# create an instance of PlanQuery from a dict
plan_query_from_dict = PlanQuery.from_dict(plan_query_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


