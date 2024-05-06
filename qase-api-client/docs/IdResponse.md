# IdResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **bool** |  | [optional] 
**result** | [**IdResponseAllOfResult**](IdResponseAllOfResult.md) |  | [optional] 

## Example

```python
from qase.api_client_v1.models.id_response import IdResponse

# TODO update the JSON string below
json = "{}"
# create an instance of IdResponse from a JSON string
id_response_instance = IdResponse.from_json(json)
# print the JSON string representation of the object
print(IdResponse.to_json())

# convert the object into a dict
id_response_dict = id_response_instance.to_dict()
# create an instance of IdResponse from a dict
id_response_form_dict = id_response.from_dict(id_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


