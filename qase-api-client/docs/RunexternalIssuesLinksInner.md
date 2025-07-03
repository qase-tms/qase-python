# RunexternalIssuesLinksInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**run_id** | **int** |  | 
**external_issue** | **str** | An external issue identifier, e.g. \&quot;PROJ-1234\&quot;. Or null if you want to remove the link. | [optional] 

## Example

```python
from qase.api_client_v1.models.runexternal_issues_links_inner import RunexternalIssuesLinksInner

# TODO update the JSON string below
json = "{}"
# create an instance of RunexternalIssuesLinksInner from a JSON string
runexternal_issues_links_inner_instance = RunexternalIssuesLinksInner.from_json(json)
# print the JSON string representation of the object
print(RunexternalIssuesLinksInner.to_json())

# convert the object into a dict
runexternal_issues_links_inner_dict = runexternal_issues_links_inner_instance.to_dict()
# create an instance of RunexternalIssuesLinksInner from a dict
runexternal_issues_links_inner_form_dict = runexternal_issues_links_inner.from_dict(runexternal_issues_links_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


