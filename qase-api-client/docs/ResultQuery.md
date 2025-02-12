# ResultQuery


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**hash** | **str** |  | [optional] 
**result_hash** | **str** |  | 
**comment** | **str** |  | [optional] 
**stacktrace** | **str** |  | [optional] 
**run_id** | **int** |  | [optional] 
**case_id** | **int** |  | [optional] 
**steps** | [**List[TestStepResult]**](TestStepResult.md) |  | [optional] 
**status** | **str** |  | [optional] 
**is_api_result** | **bool** |  | [optional] 
**time_spent_ms** | **int** |  | [optional] 
**end_time** | **datetime** |  | [optional] 
**attachments** | [**List[Attachment]**](Attachment.md) |  | [optional] 

## Example

```python
from qase.api_client_v1.models.result_query import ResultQuery

# TODO update the JSON string below
json = "{}"
# create an instance of ResultQuery from a JSON string
result_query_instance = ResultQuery.from_json(json)
# print the JSON string representation of the object
print(ResultQuery.to_json())

# convert the object into a dict
result_query_dict = result_query_instance.to_dict()
# create an instance of ResultQuery from a dict
result_query_form_dict = result_query.from_dict(result_query_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


