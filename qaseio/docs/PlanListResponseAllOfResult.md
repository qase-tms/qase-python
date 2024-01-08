# PlanListResponseAllOfResult


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**total** | **int** |  | [optional] 
**filtered** | **int** |  | [optional] 
**count** | **int** |  | [optional] 
**entities** | [**List[Plan]**](Plan.md) |  | [optional] 

## Example

```python
from qaseio.models.plan_list_response_all_of_result import PlanListResponseAllOfResult

# TODO update the JSON string below
json = "{}"
# create an instance of PlanListResponseAllOfResult from a JSON string
plan_list_response_all_of_result_instance = PlanListResponseAllOfResult.from_json(json)
# print the JSON string representation of the object
print PlanListResponseAllOfResult.to_json()

# convert the object into a dict
plan_list_response_all_of_result_dict = plan_list_response_all_of_result_instance.to_dict()
# create an instance of PlanListResponseAllOfResult from a dict
plan_list_response_all_of_result_form_dict = plan_list_response_all_of_result.from_dict(plan_list_response_all_of_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


