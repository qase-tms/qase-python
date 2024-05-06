# SuiteUpdate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**title** | **str** | Test suite title. | [optional] 
**description** | **str** | Test suite description. | [optional] 
**preconditions** | **str** | Test suite preconditions | [optional] 
**parent_id** | **int** | Parent suite ID | [optional] 

## Example

```python
from qase.api_client_v1.models.suite_update import SuiteUpdate

# TODO update the JSON string below
json = "{}"
# create an instance of SuiteUpdate from a JSON string
suite_update_instance = SuiteUpdate.from_json(json)
# print the JSON string representation of the object
print(SuiteUpdate.to_json())

# convert the object into a dict
suite_update_dict = suite_update_instance.to_dict()
# create an instance of SuiteUpdate from a dict
suite_update_form_dict = suite_update.from_dict(suite_update_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


