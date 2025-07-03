# RunexternalIssues


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** |  | 
**links** | [**List[RunexternalIssuesLinksInner]**](RunexternalIssuesLinksInner.md) | Array of external issue links. Each test run (run_id) can have only one external issue link. | 

## Example

```python
from qase.api_client_v1.models.runexternal_issues import RunexternalIssues

# TODO update the JSON string below
json = "{}"
# create an instance of RunexternalIssues from a JSON string
runexternal_issues_instance = RunexternalIssues.from_json(json)
# print the JSON string representation of the object
print(RunexternalIssues.to_json())

# convert the object into a dict
runexternal_issues_dict = runexternal_issues_instance.to_dict()
# create an instance of RunexternalIssues from a dict
runexternal_issues_form_dict = runexternal_issues.from_dict(runexternal_issues_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


