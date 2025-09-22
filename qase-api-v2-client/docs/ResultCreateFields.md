# ResultCreateFields


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**author** | **str** | Author of the related test case (member id, name or email). If set and test case auto-creation is enabled, the author will be used to create the test case | [optional] 
**description** | **str** |  | [optional] 
**preconditions** | **str** |  | [optional] 
**postconditions** | **str** |  | [optional] 
**layer** | **str** |  | [optional] 
**severity** | **str** |  | [optional] 
**priority** | **str** |  | [optional] 
**behavior** | **str** |  | [optional] 
**type** | **str** |  | [optional] 
**muted** | **str** |  | [optional] 
**is_flaky** | **str** |  | [optional] 
**executed_by** | **str** | User who executed the test (member id, name or email) | [optional] 

## Example

```python
from qase.api_client_v2.models.result_create_fields import ResultCreateFields

# TODO update the JSON string below
json = "{}"
# create an instance of ResultCreateFields from a JSON string
result_create_fields_instance = ResultCreateFields.from_json(json)
# print the JSON string representation of the object
print(ResultCreateFields.to_json())

# convert the object into a dict
result_create_fields_dict = result_create_fields_instance.to_dict()
# create an instance of ResultCreateFields from a dict
result_create_fields_from_dict = ResultCreateFields.from_dict(result_create_fields_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


