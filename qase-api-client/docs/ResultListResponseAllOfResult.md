# ResultListResponseAllOfResult


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**total** | **int** |  | [optional] 
**filtered** | **int** |  | [optional] 
**count** | **int** |  | [optional] 
**entities** | [**List[Result]**](Result.md) |  | [optional] 

## Example

```python
from qase.api_client_v1.models.result_list_response_all_of_result import ResultListResponseAllOfResult

# TODO update the JSON string below
json = "{}"
# create an instance of ResultListResponseAllOfResult from a JSON string
result_list_response_all_of_result_instance = ResultListResponseAllOfResult.from_json(json)
# print the JSON string representation of the object
print(ResultListResponseAllOfResult.to_json())

# convert the object into a dict
result_list_response_all_of_result_dict = result_list_response_all_of_result_instance.to_dict()
# create an instance of ResultListResponseAllOfResult from a dict
result_list_response_all_of_result_form_dict = result_list_response_all_of_result.from_dict(result_list_response_all_of_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


