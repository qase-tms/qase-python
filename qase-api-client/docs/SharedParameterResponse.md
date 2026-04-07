# SharedParameterResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **bool** |  | [optional] 
**result** | [**SharedParameter**](SharedParameter.md) |  | [optional] 

## Example

```python
from qase.api_client_v1.models.shared_parameter_response import SharedParameterResponse

# TODO update the JSON string below
json = "{}"
# create an instance of SharedParameterResponse from a JSON string
shared_parameter_response_instance = SharedParameterResponse.from_json(json)
# print the JSON string representation of the object
print(SharedParameterResponse.to_json())

# convert the object into a dict
shared_parameter_response_dict = shared_parameter_response_instance.to_dict()
# create an instance of SharedParameterResponse from a dict
shared_parameter_response_from_dict = SharedParameterResponse.from_dict(shared_parameter_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


