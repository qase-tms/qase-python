# ProjectCounts


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**cases** | **int** |  | [optional] 
**suites** | **int** |  | [optional] 
**milestones** | **int** |  | [optional] 
**runs** | [**ProjectCountsRuns**](ProjectCountsRuns.md) |  | [optional] 
**defects** | [**ProjectCountsDefects**](ProjectCountsDefects.md) |  | [optional] 

## Example

```python
from qase.api_client_v1.models.project_counts import ProjectCounts

# TODO update the JSON string below
json = "{}"
# create an instance of ProjectCounts from a JSON string
project_counts_instance = ProjectCounts.from_json(json)
# print the JSON string representation of the object
print(ProjectCounts.to_json())

# convert the object into a dict
project_counts_dict = project_counts_instance.to_dict()
# create an instance of ProjectCounts from a dict
project_counts_form_dict = project_counts.from_dict(project_counts_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


