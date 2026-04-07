# ProjectResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **bool** |  | [optional] 
**result** | [**Project**](Project.md) |  | [optional] 

## Example

```python
from qase.api_client_v1.models.project_response import ProjectResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ProjectResponse from a JSON string
project_response_instance = ProjectResponse.from_json(json)
# print the JSON string representation of the object
print(ProjectResponse.to_json())

# convert the object into a dict
project_response_dict = project_response_instance.to_dict()
# create an instance of ProjectResponse from a dict
project_response_from_dict = ProjectResponse.from_dict(project_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


