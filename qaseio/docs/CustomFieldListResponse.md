# CustomFieldListResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **bool** |  | [optional] 
**result** | [**CustomFieldsResponseAllOfResult**](CustomFieldsResponseAllOfResult.md) |  | [optional] 

## Example

```python
from qaseio.models.custom_field_list_response import CustomFieldListResponse

# TODO update the JSON string below
json = "{}"
# create an instance of CustomFieldListResponse from a JSON string
custom_field_list_response_instance = CustomFieldListResponse.from_json(json)
# print the JSON string representation of the object
print CustomFieldListResponse.to_json()

# convert the object into a dict
custom_field_list_response_dict = custom_field_list_response_instance.to_dict()
# create an instance of CustomFieldListResponse from a dict
custom_field_list_response_form_dict = custom_field_list_response.from_dict(custom_field_list_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


