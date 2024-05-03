# CustomFieldsResponseAllOfResult


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**total** | **int** |  | [optional] 
**filtered** | **int** |  | [optional] 
**count** | **int** |  | [optional] 
**entities** | [**List[CustomField]**](CustomField.md) |  | [optional] 

## Example

```python
from src.qase.api_client_v1.models.custom_fields_response_all_of_result import CustomFieldsResponseAllOfResult

# TODO update the JSON string below
json = "{}"
# create an instance of CustomFieldsResponseAllOfResult from a JSON string
custom_fields_response_all_of_result_instance = CustomFieldsResponseAllOfResult.from_json(json)
# print the JSON string representation of the object
print(CustomFieldsResponseAllOfResult.to_json())

# convert the object into a dict
custom_fields_response_all_of_result_dict = custom_fields_response_all_of_result_instance.to_dict()
# create an instance of CustomFieldsResponseAllOfResult from a dict
custom_fields_response_all_of_result_form_dict = custom_fields_response_all_of_result.from_dict(
    custom_fields_response_all_of_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


