# ResultListResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **bool** |  | [optional] 
**result** | [**ResultListResponseAllOfResult**](ResultListResponseAllOfResult.md) |  | [optional] 

## Example

```python
from qase.api_client_v1.models.result_list_response import ResultListResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ResultListResponse from a JSON string
result_list_response_instance = ResultListResponse.from_json(json)
# print the JSON string representation of the object
print(ResultListResponse.to_json())

# convert the object into a dict
result_list_response_dict = result_list_response_instance.to_dict()
# create an instance of ResultListResponse from a dict
result_list_response_from_dict = ResultListResponse.from_dict(result_list_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


