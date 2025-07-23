# RunCreate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**title** | **str** |  | 
**description** | **str** |  | [optional] 
**include_all_cases** | **bool** |  | [optional] 
**cases** | **List[int]** |  | [optional] 
**is_autotest** | **bool** |  | [optional] 
**environment_id** | **int** |  | [optional] 
**environment_slug** | **str** |  | [optional] 
**milestone_id** | **int** |  | [optional] 
**plan_id** | **int** |  | [optional] 
**author_id** | **int** |  | [optional] 
**tags** | **List[str]** |  | [optional] 
**configurations** | **List[int]** |  | [optional] 
**custom_field** | **Dict[str, str]** | A map of custom fields values (id &#x3D;&gt; value) | [optional] 
**start_time** | **str** |  | [optional] 
**end_time** | **str** |  | [optional] 
**is_cloud** | **bool** | Indicates if the run is created for the Test Cases produced by AIDEN | [optional] 
**cloud_run_config** | [**RunCreateCloudRunConfig**](RunCreateCloudRunConfig.md) |  | [optional] 

## Example

```python
from qase.api_client_v1.models.run_create import RunCreate

# TODO update the JSON string below
json = "{}"
# create an instance of RunCreate from a JSON string
run_create_instance = RunCreate.from_json(json)
# print the JSON string representation of the object
print(RunCreate.to_json())

# convert the object into a dict
run_create_dict = run_create_instance.to_dict()
# create an instance of RunCreate from a dict
run_create_form_dict = run_create.from_dict(run_create_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


