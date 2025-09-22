# ResultCreateResponseAllOfResult


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**case_id** | **int** |  | [optional] 
**hash** | **str** |  | [optional] 

## Example

```python
from qase.api_client_v2.models.result_create_response_all_of_result import ResultCreateResponseAllOfResult

# TODO update the JSON string below
json = "{}"
# create an instance of ResultCreateResponseAllOfResult from a JSON string
result_create_response_all_of_result_instance = ResultCreateResponseAllOfResult.from_json(json)
# print the JSON string representation of the object
print(ResultCreateResponseAllOfResult.to_json())

# convert the object into a dict
result_create_response_all_of_result_dict = result_create_response_all_of_result_instance.to_dict()
# create an instance of ResultCreateResponseAllOfResult from a dict
result_create_response_all_of_result_from_dict = ResultCreateResponseAllOfResult.from_dict(result_create_response_all_of_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


