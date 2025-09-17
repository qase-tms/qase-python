# Result


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**hash** | **str** |  | [optional] 
**result_hash** | **str** |  | [optional] 
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
from qase.api_client_v1.models.result import Result

# TODO update the JSON string below
json = "{}"
# create an instance of Result from a JSON string
result_instance = Result.from_json(json)
# print the JSON string representation of the object
print(Result.to_json())

# convert the object into a dict
result_dict = result_instance.to_dict()
# create an instance of Result from a dict
result_from_dict = Result.from_dict(result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


