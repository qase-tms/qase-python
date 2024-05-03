# BaseResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **bool** |  | [optional] 

## Example

```python
from src.qase.api_client_v1.models.base_response import BaseResponse

# TODO update the JSON string below
json = "{}"
# create an instance of BaseResponse from a JSON string
base_response_instance = BaseResponse.from_json(json)
# print the JSON string representation of the object
print(BaseResponse.to_json())

# convert the object into a dict
base_response_dict = base_response_instance.to_dict()
# create an instance of BaseResponse from a dict
base_response_form_dict = base_response.from_dict(base_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


