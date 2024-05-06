# TestCaseResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **bool** |  | [optional] 
**result** | [**TestCase**](TestCase.md) |  | [optional] 

## Example

```python
from qase.api_client_v1.models.test_case_response import TestCaseResponse

# TODO update the JSON string below
json = "{}"
# create an instance of TestCaseResponse from a JSON string
test_case_response_instance = TestCaseResponse.from_json(json)
# print the JSON string representation of the object
print(TestCaseResponse.to_json())

# convert the object into a dict
test_case_response_dict = test_case_response_instance.to_dict()
# create an instance of TestCaseResponse from a dict
test_case_response_form_dict = test_case_response.from_dict(test_case_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


