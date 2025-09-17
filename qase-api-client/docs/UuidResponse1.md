# UuidResponse1


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **bool** |  | [optional] 
**result** | [**UuidResponseAllOfResult**](UuidResponseAllOfResult.md) |  | [optional] 

## Example

```python
from qase.api_client_v1.models.uuid_response1 import UuidResponse1

# TODO update the JSON string below
json = "{}"
# create an instance of UuidResponse1 from a JSON string
uuid_response1_instance = UuidResponse1.from_json(json)
# print the JSON string representation of the object
print(UuidResponse1.to_json())

# convert the object into a dict
uuid_response1_dict = uuid_response1_instance.to_dict()
# create an instance of UuidResponse1 from a dict
uuid_response1_from_dict = UuidResponse1.from_dict(uuid_response1_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


