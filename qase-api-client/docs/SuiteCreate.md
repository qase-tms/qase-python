# SuiteCreate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**title** | **str** | Test suite title. | 
**description** | **str** | Test suite description. | [optional] 
**preconditions** | **str** | Test suite preconditions | [optional] 
**parent_id** | **int** | Parent suite ID | [optional] 

## Example

```python
from src.qase.api_client_v1.models.suite_create import SuiteCreate

# TODO update the JSON string below
json = "{}"
# create an instance of SuiteCreate from a JSON string
suite_create_instance = SuiteCreate.from_json(json)
# print the JSON string representation of the object
print(SuiteCreate.to_json())

# convert the object into a dict
suite_create_dict = suite_create_instance.to_dict()
# create an instance of SuiteCreate from a dict
suite_create_form_dict = suite_create.from_dict(suite_create_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


