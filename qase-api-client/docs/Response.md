# Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **bool** |  | [optional] 

## Example

```python
from qase.api_client_v1.models.response import Response

# TODO update the JSON string below
json = "{}"
# create an instance of Response from a JSON string
response_instance = Response.from_json(json)
# print the JSON string representation of the object
print(Response.to_json())

# convert the object into a dict
response_dict = response_instance.to_dict()
# create an instance of Response from a dict
response_from_dict = Response.from_dict(response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


