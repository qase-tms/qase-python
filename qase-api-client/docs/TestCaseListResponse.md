# TestCaseListResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **bool** |  | [optional] 
**result** | [**TestCaseListResponseAllOfResult**](TestCaseListResponseAllOfResult.md) |  | [optional] 

## Example

```python
from qase.api_client_v1.models.test_case_list_response import TestCaseListResponse

# TODO update the JSON string below
json = "{}"
# create an instance of TestCaseListResponse from a JSON string
test_case_list_response_instance = TestCaseListResponse.from_json(json)
# print the JSON string representation of the object
print(TestCaseListResponse.to_json())

# convert the object into a dict
test_case_list_response_dict = test_case_list_response_instance.to_dict()
# create an instance of TestCaseListResponse from a dict
test_case_list_response_form_dict = test_case_list_response.from_dict(test_case_list_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


