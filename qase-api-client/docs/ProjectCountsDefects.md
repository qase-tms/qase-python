# ProjectCountsDefects


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**total** | **int** |  | [optional] 
**open** | **int** |  | [optional] 

## Example

```python
from src.qase.api_client_v1.models.project_counts_defects import ProjectCountsDefects

# TODO update the JSON string below
json = "{}"
# create an instance of ProjectCountsDefects from a JSON string
project_counts_defects_instance = ProjectCountsDefects.from_json(json)
# print the JSON string representation of the object
print(ProjectCountsDefects.to_json())

# convert the object into a dict
project_counts_defects_dict = project_counts_defects_instance.to_dict()
# create an instance of ProjectCountsDefects from a dict
project_counts_defects_form_dict = project_counts_defects.from_dict(project_counts_defects_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


