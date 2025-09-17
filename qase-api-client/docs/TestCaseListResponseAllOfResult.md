# TestCaseListResponseAllOfResult


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**total** | **int** |  | [optional] 
**filtered** | **int** |  | [optional] 
**count** | **int** |  | [optional] 
**entities** | [**List[TestCase]**](TestCase.md) |  | [optional] 

## Example

```python
from qase.api_client_v1.models.test_case_list_response_all_of_result import TestCaseListResponseAllOfResult

# TODO update the JSON string below
json = "{}"
# create an instance of TestCaseListResponseAllOfResult from a JSON string
test_case_list_response_all_of_result_instance = TestCaseListResponseAllOfResult.from_json(json)
# print the JSON string representation of the object
print(TestCaseListResponseAllOfResult.to_json())

# convert the object into a dict
test_case_list_response_all_of_result_dict = test_case_list_response_all_of_result_instance.to_dict()
# create an instance of TestCaseListResponseAllOfResult from a dict
test_case_list_response_all_of_result_from_dict = TestCaseListResponseAllOfResult.from_dict(test_case_list_response_all_of_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


