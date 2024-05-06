# ProjectCreate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**title** | **str** | Project title. | 
**code** | **str** | Project code. Unique for team. Digits and special characters are not allowed. | 
**description** | **str** | Project description. | [optional] 
**access** | **str** |  | [optional] 
**group** | **str** | Team group hash. Required if access param is set to group. | [optional] 
**settings** | **Dict[str, object]** | Additional project settings. | [optional] 

## Example

```python
from qase.api_client_v1.models.project_create import ProjectCreate

# TODO update the JSON string below
json = "{}"
# create an instance of ProjectCreate from a JSON string
project_create_instance = ProjectCreate.from_json(json)
# print the JSON string representation of the object
print(ProjectCreate.to_json())

# convert the object into a dict
project_create_dict = project_create_instance.to_dict()
# create an instance of ProjectCreate from a dict
project_create_form_dict = project_create.from_dict(project_create_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


