# Project


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**title** | **str** |  | [optional] 
**code** | **str** |  | [optional] 
**counts** | [**ProjectCounts**](ProjectCounts.md) |  | [optional] 

## Example

```python
from qase.api_client_v1.models.project import Project

# TODO update the JSON string below
json = "{}"
# create an instance of Project from a JSON string
project_instance = Project.from_json(json)
# print the JSON string representation of the object
print(Project.to_json())

# convert the object into a dict
project_dict = project_instance.to_dict()
# create an instance of Project from a dict
project_from_dict = Project.from_dict(project_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


