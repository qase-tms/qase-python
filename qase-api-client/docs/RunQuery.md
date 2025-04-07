# RunQuery


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | [optional] 
**run_id** | **int** |  | 
**title** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**status** | **int** |  | [optional] 
**status_text** | **str** |  | [optional] 
**start_time** | **datetime** |  | [optional] 
**end_time** | **datetime** |  | [optional] 
**public** | **bool** |  | [optional] 
**stats** | [**RunStats**](RunStats.md) |  | [optional] 
**time_spent** | **int** | Time in ms. | [optional] 
**elapsed_time** | **int** | Time in ms. | [optional] 
**environment** | [**RunEnvironment**](RunEnvironment.md) |  | [optional] 
**milestone** | [**RunMilestone**](RunMilestone.md) |  | [optional] 
**custom_fields** | [**List[CustomFieldValue]**](CustomFieldValue.md) |  | [optional] 
**tags** | [**List[TagValue]**](TagValue.md) |  | [optional] 
**cases** | **List[int]** |  | [optional] 
**plan_id** | **int** |  | [optional] 

## Example

```python
from qase.api_client_v1.models.run_query import RunQuery

# TODO update the JSON string below
json = "{}"
# create an instance of RunQuery from a JSON string
run_query_instance = RunQuery.from_json(json)
# print the JSON string representation of the object
print(RunQuery.to_json())

# convert the object into a dict
run_query_dict = run_query_instance.to_dict()
# create an instance of RunQuery from a dict
run_query_form_dict = run_query.from_dict(run_query_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


