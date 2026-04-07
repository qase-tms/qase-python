# ProjectListResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **bool** |  | [optional] 
**result** | [**ProjectListResponseAllOfResult**](ProjectListResponseAllOfResult.md) |  | [optional] 

## Example

```python
from qase.api_client_v1.models.project_list_response import ProjectListResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ProjectListResponse from a JSON string
project_list_response_instance = ProjectListResponse.from_json(json)
# print the JSON string representation of the object
print(ProjectListResponse.to_json())

# convert the object into a dict
project_list_response_dict = project_list_response_instance.to_dict()
# create an instance of ProjectListResponse from a dict
project_list_response_from_dict = ProjectListResponse.from_dict(project_list_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


