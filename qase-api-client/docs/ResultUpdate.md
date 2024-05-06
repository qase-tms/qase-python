# ResultUpdate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **str** |  | [optional] 
**time_ms** | **int** |  | [optional] 
**defect** | **bool** |  | [optional] 
**attachments** | **List[str]** |  | [optional] 
**stacktrace** | **str** |  | [optional] 
**comment** | **str** |  | [optional] 
**steps** | [**List[TestStepResultCreate]**](TestStepResultCreate.md) |  | [optional] 

## Example

```python
from qase.api_client_v1.models.result_update import ResultUpdate

# TODO update the JSON string below
json = "{}"
# create an instance of ResultUpdate from a JSON string
result_update_instance = ResultUpdate.from_json(json)
# print the JSON string representation of the object
print(ResultUpdate.to_json())

# convert the object into a dict
result_update_dict = result_update_instance.to_dict()
# create an instance of ResultUpdate from a dict
result_update_form_dict = result_update.from_dict(result_update_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


