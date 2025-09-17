# TestCaseExternalIssues


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** |  | 
**links** | [**List[TestCaseExternalIssuesLinksInner]**](TestCaseExternalIssuesLinksInner.md) |  | 

## Example

```python
from qase.api_client_v1.models.test_case_external_issues import TestCaseExternalIssues

# TODO update the JSON string below
json = "{}"
# create an instance of TestCaseExternalIssues from a JSON string
test_case_external_issues_instance = TestCaseExternalIssues.from_json(json)
# print the JSON string representation of the object
print(TestCaseExternalIssues.to_json())

# convert the object into a dict
test_case_external_issues_dict = test_case_external_issues_instance.to_dict()
# create an instance of TestCaseExternalIssues from a dict
test_case_external_issues_from_dict = TestCaseExternalIssues.from_dict(test_case_external_issues_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


