# SuiteListResponseAllOfResult


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**total** | **int** |  | [optional] 
**filtered** | **int** |  | [optional] 
**count** | **int** |  | [optional] 
**entities** | [**List[Suite]**](Suite.md) |  | [optional] 

## Example

```python
from qase.api_client_v1.models.suite_list_response_all_of_result import SuiteListResponseAllOfResult

# TODO update the JSON string below
json = "{}"
# create an instance of SuiteListResponseAllOfResult from a JSON string
suite_list_response_all_of_result_instance = SuiteListResponseAllOfResult.from_json(json)
# print the JSON string representation of the object
print(SuiteListResponseAllOfResult.to_json())

# convert the object into a dict
suite_list_response_all_of_result_dict = suite_list_response_all_of_result_instance.to_dict()
# create an instance of SuiteListResponseAllOfResult from a dict
suite_list_response_all_of_result_from_dict = SuiteListResponseAllOfResult.from_dict(suite_list_response_all_of_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


