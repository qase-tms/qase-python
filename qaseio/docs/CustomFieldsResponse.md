# CustomFieldsResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **bool** |  | [optional] 
**result** | [**CustomFieldsResponseAllOfResult**](CustomFieldsResponseAllOfResult.md) |  | [optional] 

## Example

```python
from qaseio.models.custom_fields_response import CustomFieldsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of CustomFieldsResponse from a JSON string
custom_fields_response_instance = CustomFieldsResponse.from_json(json)
# print the JSON string representation of the object
print CustomFieldsResponse.to_json()

# convert the object into a dict
custom_fields_response_dict = custom_fields_response_instance.to_dict()
# create an instance of CustomFieldsResponse from a dict
custom_fields_response_form_dict = custom_fields_response.from_dict(custom_fields_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


