# ProjectListResponseAllOfResult


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**total** | **int** |  | [optional] 
**filtered** | **int** |  | [optional] 
**count** | **int** |  | [optional] 
**entities** | [**List[Project]**](Project.md) |  | [optional] 

## Example

```python
from qase.api_client_v1.models.project_list_response_all_of_result import ProjectListResponseAllOfResult

# TODO update the JSON string below
json = "{}"
# create an instance of ProjectListResponseAllOfResult from a JSON string
project_list_response_all_of_result_instance = ProjectListResponseAllOfResult.from_json(json)
# print the JSON string representation of the object
print(ProjectListResponseAllOfResult.to_json())

# convert the object into a dict
project_list_response_all_of_result_dict = project_list_response_all_of_result_instance.to_dict()
# create an instance of ProjectListResponseAllOfResult from a dict
project_list_response_all_of_result_form_dict = project_list_response_all_of_result.from_dict(
    project_list_response_all_of_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


