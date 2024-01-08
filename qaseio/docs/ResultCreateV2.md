# ResultCreateV2


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | If passed, used as an idempotency key | [optional] 
**title** | **str** |  | 
**signature** | **str** |  | [optional] 
**testops_id** | **int** |  | [optional] 
**execution** | [**ResultExecution**](ResultExecution.md) |  | 
**fields** | **Dict[str, str]** |  | [optional] 
**attachments** | [**List[ResultAttachment]**](ResultAttachment.md) |  | [optional] 
**steps** | [**List[ResultStep]**](ResultStep.md) |  | [optional] 
**params** | **Dict[str, str]** |  | [optional] 
**author** | **str** |  | [optional] 
**relations** | [**ResultRelations**](ResultRelations.md) |  | [optional] 
**muted** | **bool** |  | [optional] 
**message** | **str** |  | [optional] 
**created_at** | **float** |  | [optional] 

## Example

```python
from qaseio.models.result_create_v2 import ResultCreateV2

# TODO update the JSON string below
json = "{}"
# create an instance of ResultCreateV2 from a JSON string
result_create_v2_instance = ResultCreateV2.from_json(json)
# print the JSON string representation of the object
print ResultCreateV2.to_json()

# convert the object into a dict
result_create_v2_dict = result_create_v2_instance.to_dict()
# create an instance of ResultCreateV2 from a dict
result_create_v2_form_dict = result_create_v2.from_dict(result_create_v2_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


