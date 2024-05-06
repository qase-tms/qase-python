# ExternalIssue


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** |  | [optional] 
**issues** | [**List[ExternalIssueIssuesInner]**](ExternalIssueIssuesInner.md) |  | [optional] 

## Example

```python
from qase.api_client_v1.models.external_issue import ExternalIssue

# TODO update the JSON string below
json = "{}"
# create an instance of ExternalIssue from a JSON string
external_issue_instance = ExternalIssue.from_json(json)
# print the JSON string representation of the object
print(ExternalIssue.to_json())

# convert the object into a dict
external_issue_dict = external_issue_instance.to_dict()
# create an instance of ExternalIssue from a dict
external_issue_form_dict = external_issue.from_dict(external_issue_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


