# RunExternalIssue


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | [optional] 
**type** | **str** |  | [optional] 
**link** | **str** |  | [optional] 

## Example

```python
from qase.api_client_v1.models.run_external_issue import RunExternalIssue

# TODO update the JSON string below
json = "{}"
# create an instance of RunExternalIssue from a JSON string
run_external_issue_instance = RunExternalIssue.from_json(json)
# print the JSON string representation of the object
print(RunExternalIssue.to_json())

# convert the object into a dict
run_external_issue_dict = run_external_issue_instance.to_dict()
# create an instance of RunExternalIssue from a dict
run_external_issue_form_dict = run_external_issue.from_dict(run_external_issue_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


