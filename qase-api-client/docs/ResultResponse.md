# ResultResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **bool** |  | [optional] 
**result** | [**Result**](Result.md) |  | [optional] 

## Example

```python
from qase.api_client_v1.models.result_response import ResultResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ResultResponse from a JSON string
result_response_instance = ResultResponse.from_json(json)
# print the JSON string representation of the object
print(ResultResponse.to_json())

# convert the object into a dict
result_response_dict = result_response_instance.to_dict()
# create an instance of ResultResponse from a dict
result_response_from_dict = ResultResponse.from_dict(result_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


