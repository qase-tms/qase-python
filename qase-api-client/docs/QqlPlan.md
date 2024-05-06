# QqlPlan


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
from qase.api_client_v1.models.qql_plan import QqlPlan

# TODO update the JSON string below
json = "{}"
# create an instance of QqlPlan from a JSON string
qql_plan_instance = QqlPlan.from_json(json)
# print the JSON string representation of the object
print(QqlPlan.to_json())

# convert the object into a dict
qql_plan_dict = qql_plan_instance.to_dict()
# create an instance of QqlPlan from a dict
qql_plan_form_dict = qql_plan.from_dict(qql_plan_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


