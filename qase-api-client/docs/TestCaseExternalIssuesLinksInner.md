# TestCaseExternalIssuesLinksInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**case_id** | **int** |  | 
**external_issues** | **List[str]** |  | 

## Example

```python
from qase.api_client_v1.models.test_case_external_issues_links_inner import TestCaseExternalIssuesLinksInner

# TODO update the JSON string below
json = "{}"
# create an instance of TestCaseExternalIssuesLinksInner from a JSON string
test_case_external_issues_links_inner_instance = TestCaseExternalIssuesLinksInner.from_json(json)
# print the JSON string representation of the object
print(TestCaseExternalIssuesLinksInner.to_json())

# convert the object into a dict
test_case_external_issues_links_inner_dict = test_case_external_issues_links_inner_instance.to_dict()
# create an instance of TestCaseExternalIssuesLinksInner from a dict
test_case_external_issues_links_inner_form_dict = test_case_external_issues_links_inner.from_dict(test_case_external_issues_links_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


