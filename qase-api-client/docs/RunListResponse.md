# RunListResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **bool** |  | [optional] 
**result** | [**RunListResponseAllOfResult**](RunListResponseAllOfResult.md) |  | [optional] 

## Example

```python
from qase.api_client_v1.models.run_list_response import RunListResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RunListResponse from a JSON string
run_list_response_instance = RunListResponse.from_json(json)
# print the JSON string representation of the object
print(RunListResponse.to_json())

# convert the object into a dict
run_list_response_dict = run_list_response_instance.to_dict()
# create an instance of RunListResponse from a dict
run_list_response_from_dict = RunListResponse.from_dict(run_list_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


