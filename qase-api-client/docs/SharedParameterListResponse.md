# SharedParameterListResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **bool** |  | [optional] 
**result** | [**SharedParameterListResponseAllOfResult**](SharedParameterListResponseAllOfResult.md) |  | [optional] 

## Example

```python
from qase.api_client_v1.models.shared_parameter_list_response import SharedParameterListResponse

# TODO update the JSON string below
json = "{}"
# create an instance of SharedParameterListResponse from a JSON string
shared_parameter_list_response_instance = SharedParameterListResponse.from_json(json)
# print the JSON string representation of the object
print(SharedParameterListResponse.to_json())

# convert the object into a dict
shared_parameter_list_response_dict = shared_parameter_list_response_instance.to_dict()
# create an instance of SharedParameterListResponse from a dict
shared_parameter_list_response_from_dict = SharedParameterListResponse.from_dict(shared_parameter_list_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


