# RunExternalIssues


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** |  | 
**links** | [**List[RunExternalIssuesLinksInner]**](RunExternalIssuesLinksInner.md) | Array of external issue links. Each test run (run_id) can have only one external issue link. | 

## Example

```python
from qase.api_client_v1.models.run_external_issues import RunExternalIssues

# TODO update the JSON string below
json = "{}"
# create an instance of RunExternalIssues from a JSON string
run_external_issues_instance = RunExternalIssues.from_json(json)
# print the JSON string representation of the object
print(RunExternalIssues.to_json())

# convert the object into a dict
run_external_issues_dict = run_external_issues_instance.to_dict()
# create an instance of RunExternalIssues from a dict
run_external_issues_from_dict = RunExternalIssues.from_dict(run_external_issues_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


