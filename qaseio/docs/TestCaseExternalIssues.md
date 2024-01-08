# TestCaseexternalIssues


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** |  | 
**links** | [**List[TestCaseExternalIssuesLinksInner]**](TestCaseExternalIssuesLinksInner.md) |  | 

## Example

```python
from qaseio.models.test_caseexternal_issues import TestCaseexternalIssues

# TODO update the JSON string below
json = "{}"
# create an instance of TestCaseexternalIssues from a JSON string
test_caseexternal_issues_instance = TestCaseexternalIssues.from_json(json)
# print the JSON string representation of the object
print TestCaseexternalIssues.to_json()

# convert the object into a dict
test_caseexternal_issues_dict = test_caseexternal_issues_instance.to_dict()
# create an instance of TestCaseexternalIssues from a dict
test_caseexternal_issues_form_dict = test_caseexternal_issues.from_dict(test_caseexternal_issues_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


