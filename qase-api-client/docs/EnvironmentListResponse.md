# EnvironmentListResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **bool** |  | [optional] 
**result** | [**EnvironmentListResponseAllOfResult**](EnvironmentListResponseAllOfResult.md) |  | [optional] 

## Example

```python
from src.qase.api_client_v1.models.environment_list_response import EnvironmentListResponse

# TODO update the JSON string below
json = "{}"
# create an instance of EnvironmentListResponse from a JSON string
environment_list_response_instance = EnvironmentListResponse.from_json(json)
# print the JSON string representation of the object
print(EnvironmentListResponse.to_json())

# convert the object into a dict
environment_list_response_dict = environment_list_response_instance.to_dict()
# create an instance of EnvironmentListResponse from a dict
environment_list_response_form_dict = environment_list_response.from_dict(environment_list_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


