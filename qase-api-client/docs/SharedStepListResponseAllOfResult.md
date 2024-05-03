# SharedStepListResponseAllOfResult


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**total** | **int** |  | [optional] 
**filtered** | **int** |  | [optional] 
**count** | **int** |  | [optional] 
**entities** | [**List[SharedStep]**](SharedStep.md) |  | [optional] 

## Example

```python
from src.qase.api_client_v1.models.shared_step_list_response_all_of_result import SharedStepListResponseAllOfResult

# TODO update the JSON string below
json = "{}"
# create an instance of SharedStepListResponseAllOfResult from a JSON string
shared_step_list_response_all_of_result_instance = SharedStepListResponseAllOfResult.from_json(json)
# print the JSON string representation of the object
print(SharedStepListResponseAllOfResult.to_json())

# convert the object into a dict
shared_step_list_response_all_of_result_dict = shared_step_list_response_all_of_result_instance.to_dict()
# create an instance of SharedStepListResponseAllOfResult from a dict
shared_step_list_response_all_of_result_form_dict = shared_step_list_response_all_of_result.from_dict(
    shared_step_list_response_all_of_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


