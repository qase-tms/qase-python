# ResultStepExecution


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**start_time** | **float** |  | [optional] 
**end_time** | **float** |  | [optional] 
**status** | [**ResultStepStatus**](ResultStepStatus.md) |  | 
**duration** | **int** |  | [optional] 
**comment** | **str** |  | [optional] 
**attachments** | **List[str]** |  | [optional] 

## Example

```python
from src.qase.models import ResultStepExecution

# TODO update the JSON string below
json = "{}"
# create an instance of ResultStepExecution from a JSON string
result_step_execution_instance = ResultStepExecution.from_json(json)
# print the JSON string representation of the object
print(ResultStepExecution.to_json())

# convert the object into a dict
result_step_execution_dict = result_step_execution_instance.to_dict()
# create an instance of ResultStepExecution from a dict
result_step_execution_form_dict = result_step_execution.from_dict(result_step_execution_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


