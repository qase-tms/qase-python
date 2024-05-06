# Bulk200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **bool** |  | [optional] 
**result** | [**Bulk200ResponseAllOfResult**](Bulk200ResponseAllOfResult.md) |  | [optional] 

## Example

```python
from qase.api_client_v1.models.bulk200_response import Bulk200Response

# TODO update the JSON string below
json = "{}"
# create an instance of Bulk200Response from a JSON string
bulk200_response_instance = Bulk200Response.from_json(json)
# print the JSON string representation of the object
print(Bulk200Response.to_json())

# convert the object into a dict
bulk200_response_dict = bulk200_response_instance.to_dict()
# create an instance of Bulk200Response from a dict
bulk200_response_form_dict = bulk200_response.from_dict(bulk200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


