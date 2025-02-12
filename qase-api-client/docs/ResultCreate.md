# ResultCreate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**case_id** | **int** |  | [optional] 
**case** | [**ResultCreateCase**](ResultCreateCase.md) |  | [optional] 
**status** | **str** | Can have the following values &#x60;passed&#x60;, &#x60;failed&#x60;, &#x60;blocked&#x60;, &#x60;skipped&#x60;, &#x60;invalid&#x60; + custom statuses | 
**start_time** | **int** |  | [optional] 
**time** | **int** |  | [optional] 
**time_ms** | **int** |  | [optional] 
**defect** | **bool** |  | [optional] 
**attachments** | **List[str]** |  | [optional] 
**stacktrace** | **str** |  | [optional] 
**comment** | **str** |  | [optional] 
**param** | **Dict[str, str]** | A map of parameters (name &#x3D;&gt; value) | [optional] 
**param_groups** | **List[List[str]]** | List parameter groups by name only. Add their values in the &#39;param&#39; field | [optional] 
**steps** | [**List[TestStepResultCreate]**](TestStepResultCreate.md) |  | [optional] 
**author_id** | **int** |  | [optional] 

## Example

```python
from qase.api_client_v1.models.result_create import ResultCreate

# TODO update the JSON string below
json = "{}"
# create an instance of ResultCreate from a JSON string
result_create_instance = ResultCreate.from_json(json)
# print the JSON string representation of the object
print(ResultCreate.to_json())

# convert the object into a dict
result_create_dict = result_create_instance.to_dict()
# create an instance of ResultCreate from a dict
result_create_form_dict = result_create.from_dict(result_create_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


