# RunListResponseAllOfResult


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**total** | **int** |  | [optional] 
**filtered** | **int** |  | [optional] 
**count** | **int** |  | [optional] 
**entities** | [**List[Run]**](Run.md) |  | [optional] 

## Example

```python
from qase.api_client_v1.models.run_list_response_all_of_result import RunListResponseAllOfResult

# TODO update the JSON string below
json = "{}"
# create an instance of RunListResponseAllOfResult from a JSON string
run_list_response_all_of_result_instance = RunListResponseAllOfResult.from_json(json)
# print the JSON string representation of the object
print(RunListResponseAllOfResult.to_json())

# convert the object into a dict
run_list_response_all_of_result_dict = run_list_response_all_of_result_instance.to_dict()
# create an instance of RunListResponseAllOfResult from a dict
run_list_response_all_of_result_form_dict = run_list_response_all_of_result.from_dict(
    run_list_response_all_of_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


