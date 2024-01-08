# ProjectCountsRuns


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**total** | **int** |  | [optional] 
**active** | **int** |  | [optional] 

## Example

```python
from qaseio.models.project_counts_runs import ProjectCountsRuns

# TODO update the JSON string below
json = "{}"
# create an instance of ProjectCountsRuns from a JSON string
project_counts_runs_instance = ProjectCountsRuns.from_json(json)
# print the JSON string representation of the object
print ProjectCountsRuns.to_json()

# convert the object into a dict
project_counts_runs_dict = project_counts_runs_instance.to_dict()
# create an instance of ProjectCountsRuns from a dict
project_counts_runs_form_dict = project_counts_runs.from_dict(project_counts_runs_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


