# ProjectCodeResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **bool** |  | [optional] 
**result** | [**ProjectCodeResponseAllOfResult**](ProjectCodeResponseAllOfResult.md) |  | [optional] 

## Example

```python
from src.qase.api_client_v1.models.project_code_response import ProjectCodeResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ProjectCodeResponse from a JSON string
project_code_response_instance = ProjectCodeResponse.from_json(json)
# print the JSON string representation of the object
print(ProjectCodeResponse.to_json())

# convert the object into a dict
project_code_response_dict = project_code_response_instance.to_dict()
# create an instance of ProjectCodeResponse from a dict
project_code_response_form_dict = project_code_response.from_dict(project_code_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


