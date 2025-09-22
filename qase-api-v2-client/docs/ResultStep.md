# ResultStep


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**ResultStepData**](ResultStepData.md) |  | [optional] 
**execution** | [**ResultStepExecution**](ResultStepExecution.md) |  | [optional] 
**steps** | **List[object]** | Nested steps will be here. The same structure is used for them. | [optional] 

## Example

```python
from qase.api_client_v2.models.result_step import ResultStep

# TODO update the JSON string below
json = "{}"
# create an instance of ResultStep from a JSON string
result_step_instance = ResultStep.from_json(json)
# print the JSON string representation of the object
print(ResultStep.to_json())

# convert the object into a dict
result_step_dict = result_step_instance.to_dict()
# create an instance of ResultStep from a dict
result_step_from_dict = ResultStep.from_dict(result_step_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


