# ResultCreateResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **bool** |  | [optional] 
**result** | [**ResultCreateResponseAllOfResult**](ResultCreateResponseAllOfResult.md) |  | [optional] 

## Example

```python
from qase.api_client_v1.models.result_create_response import ResultCreateResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ResultCreateResponse from a JSON string
result_create_response_instance = ResultCreateResponse.from_json(json)
# print the JSON string representation of the object
print(ResultCreateResponse.to_json())

# convert the object into a dict
result_create_response_dict = result_create_response_instance.to_dict()
# create an instance of ResultCreateResponse from a dict
result_create_response_form_dict = result_create_response.from_dict(result_create_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


