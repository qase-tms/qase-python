# PlanDetailed


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | [optional] 
**title** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**cases_count** | **int** |  | [optional] 
**created_at** | **datetime** |  | [optional] 
**updated_at** | **datetime** |  | [optional] 
**created** | **str** | Deprecated, use the &#x60;created_at&#x60; property instead. | [optional] 
**updated** | **str** | Deprecated, use the &#x60;updated_at&#x60; property instead. | [optional] 
**average_time** | **float** |  | [optional] 
**cases** | [**List[PlanDetailedAllOfCases]**](PlanDetailedAllOfCases.md) |  | [optional] 

## Example

```python
from qase.api_client_v1.models.plan_detailed import PlanDetailed

# TODO update the JSON string below
json = "{}"
# create an instance of PlanDetailed from a JSON string
plan_detailed_instance = PlanDetailed.from_json(json)
# print the JSON string representation of the object
print(PlanDetailed.to_json())

# convert the object into a dict
plan_detailed_dict = plan_detailed_instance.to_dict()
# create an instance of PlanDetailed from a dict
plan_detailed_form_dict = plan_detailed.from_dict(plan_detailed_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


