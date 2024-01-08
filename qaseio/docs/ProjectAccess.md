# ProjectAccess


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**member_id** | **int** | Team member id title. | [optional] 

## Example

```python
from qaseio.models.project_access import ProjectAccess

# TODO update the JSON string below
json = "{}"
# create an instance of ProjectAccess from a JSON string
project_access_instance = ProjectAccess.from_json(json)
# print the JSON string representation of the object
print ProjectAccess.to_json()

# convert the object into a dict
project_access_dict = project_access_instance.to_dict()
# create an instance of ProjectAccess from a dict
project_access_form_dict = project_access.from_dict(project_access_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


