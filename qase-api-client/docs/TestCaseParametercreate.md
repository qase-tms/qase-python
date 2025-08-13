# TestCaseParametercreate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**shared_id** | **str** |  | 
**title** | **str** |  | 
**values** | **List[str]** |  | 
**items** | [**List[ParameterSingle]**](ParameterSingle.md) |  | 

## Example

```python
from qase.api_client_v1.models.test_case_parametercreate import TestCaseParametercreate

# TODO update the JSON string below
json = "{}"
# create an instance of TestCaseParametercreate from a JSON string
test_case_parametercreate_instance = TestCaseParametercreate.from_json(json)
# print the JSON string representation of the object
print(TestCaseParametercreate.to_json())

# convert the object into a dict
test_case_parametercreate_dict = test_case_parametercreate_instance.to_dict()
# create an instance of TestCaseParametercreate from a dict
test_case_parametercreate_form_dict = test_case_parametercreate.from_dict(test_case_parametercreate_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


