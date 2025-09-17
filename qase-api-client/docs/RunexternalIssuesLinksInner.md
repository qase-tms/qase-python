# RunExternalIssuesLinksInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**run_id** | **int** |  | 
**external_issue** | **str** | An external issue identifier, e.g. \&quot;PROJ-1234\&quot;. Or null if you want to remove the link. | [optional] 

## Example

```python
from qase.api_client_v1.models.run_external_issues_links_inner import RunExternalIssuesLinksInner

# TODO update the JSON string below
json = "{}"
# create an instance of RunExternalIssuesLinksInner from a JSON string
run_external_issues_links_inner_instance = RunExternalIssuesLinksInner.from_json(json)
# print the JSON string representation of the object
print(RunExternalIssuesLinksInner.to_json())

# convert the object into a dict
run_external_issues_links_inner_dict = run_external_issues_links_inner_instance.to_dict()
# create an instance of RunExternalIssuesLinksInner from a dict
run_external_issues_links_inner_from_dict = RunExternalIssuesLinksInner.from_dict(run_external_issues_links_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


