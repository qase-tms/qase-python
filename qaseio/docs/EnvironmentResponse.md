# EnvironmentResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **bool** |  | [optional] 
**result** | [**Environment**](Environment.md) |  | [optional] 

## Example

```python
from qaseio.models.environment_response import EnvironmentResponse

# TODO update the JSON string below
json = "{}"
# create an instance of EnvironmentResponse from a JSON string
environment_response_instance = EnvironmentResponse.from_json(json)
# print the JSON string representation of the object
print EnvironmentResponse.to_json()

# convert the object into a dict
environment_response_dict = environment_response_instance.to_dict()
# create an instance of EnvironmentResponse from a dict
environment_response_form_dict = environment_response.from_dict(environment_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


