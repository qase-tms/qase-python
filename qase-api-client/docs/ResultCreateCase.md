# ResultCreateCase

Could be used instead of `case_id`.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**title** | **str** |  | [optional] 
**suite_title** | **str** | Nested suites should be separated with &#x60;TAB&#x60; symbol. | [optional] 
**description** | **str** |  | [optional] 
**preconditions** | **str** |  | [optional] 
**postconditions** | **str** |  | [optional] 
**layer** | **str** | Slug of the layer. You can get it in the System Field settings. | [optional] 
**severity** | **str** | Slug of the severity. You can get it in the System Field settings. | [optional] 
**priority** | **str** | Slug of the priority. You can get it in the System Field settings. | [optional] 

## Example

```python
from qase.api_client_v1.models.result_create_case import ResultCreateCase

# TODO update the JSON string below
json = "{}"
# create an instance of ResultCreateCase from a JSON string
result_create_case_instance = ResultCreateCase.from_json(json)
# print the JSON string representation of the object
print(ResultCreateCase.to_json())

# convert the object into a dict
result_create_case_dict = result_create_case_instance.to_dict()
# create an instance of ResultCreateCase from a dict
result_create_case_form_dict = result_create_case.from_dict(result_create_case_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


