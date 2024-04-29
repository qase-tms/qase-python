# ResultCreate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | If passed, used as an idempotency key | [optional] 
**title** | **str** |  | 
**signature** | **str** |  | [optional] 
**testops_id** | **int** |  | [optional] 
**execution** | [**ResultExecution**](ResultExecution.md) |  | 
**fields** | **Dict[str, str]** |  | [optional] 
**attachments** | **List[str]** |  | [optional] 
**steps** | [**List[ResultStep]**](ResultStep.md) |  | [optional] 
**steps_type** | [**ResultStepsType**](ResultStepsType.md) |  | [optional] 
**params** | **Dict[str, str]** |  | [optional] 
**author** | **str** |  | [optional] 
**relations** | [**ResultRelations**](ResultRelations.md) |  | [optional] 
**muted** | **bool** |  | [optional] 
**message** | **str** |  | [optional] 
**created_at** | **float** |  | [optional] 

## Example

```python
from src.qase.models import ResultCreate

# TODO update the JSON string below
json = "{}"
# create an instance of ResultCreate from a JSON string
result_create_instance = ResultCreate.from_json(json)
# print the JSON string representation of the object
print(ResultCreate.to_json())

# convert the object into a dict
result_create_dict = result_create_instance.to_dict()
# create an instance of ResultCreate from a dict
result_create_form_dict = result_create.from_dict(result_create_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


