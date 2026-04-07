# Plan


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

## Example

```python
from qase.api_client_v1.models.plan import Plan

# TODO update the JSON string below
json = "{}"
# create an instance of Plan from a JSON string
plan_instance = Plan.from_json(json)
# print the JSON string representation of the object
print(Plan.to_json())

# convert the object into a dict
plan_dict = plan_instance.to_dict()
# create an instance of Plan from a dict
plan_from_dict = Plan.from_dict(plan_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


