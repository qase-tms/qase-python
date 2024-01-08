# SystemFieldListResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **bool** |  | [optional] 
**result** | [**List[SystemField]**](SystemField.md) |  | [optional] 

## Example

```python
from qaseio.models.system_field_list_response import SystemFieldListResponse

# TODO update the JSON string below
json = "{}"
# create an instance of SystemFieldListResponse from a JSON string
system_field_list_response_instance = SystemFieldListResponse.from_json(json)
# print the JSON string representation of the object
print SystemFieldListResponse.to_json()

# convert the object into a dict
system_field_list_response_dict = system_field_list_response_instance.to_dict()
# create an instance of SystemFieldListResponse from a dict
system_field_list_response_form_dict = system_field_list_response.from_dict(system_field_list_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


