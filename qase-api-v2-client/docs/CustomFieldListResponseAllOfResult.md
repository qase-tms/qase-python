# CustomFieldListResponseAllOfResult


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**total** | **int** |  | [optional] 
**filtered** | **int** |  | [optional] 
**count** | **int** |  | [optional] 
**entities** | [**List[CustomField]**](CustomField.md) |  | [optional] 

## Example

```python
from qase.api_client_v2.models.custom_field_list_response_all_of_result import CustomFieldListResponseAllOfResult

# TODO update the JSON string below
json = "{}"
# create an instance of CustomFieldListResponseAllOfResult from a JSON string
custom_field_list_response_all_of_result_instance = CustomFieldListResponseAllOfResult.from_json(json)
# print the JSON string representation of the object
print(CustomFieldListResponseAllOfResult.to_json())

# convert the object into a dict
custom_field_list_response_all_of_result_dict = custom_field_list_response_all_of_result_instance.to_dict()
# create an instance of CustomFieldListResponseAllOfResult from a dict
custom_field_list_response_all_of_result_from_dict = CustomFieldListResponseAllOfResult.from_dict(custom_field_list_response_all_of_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


