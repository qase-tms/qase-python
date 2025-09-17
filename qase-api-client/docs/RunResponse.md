# RunResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **bool** |  | [optional] 
**result** | [**Run**](Run.md) |  | [optional] 

## Example

```python
from qase.api_client_v1.models.run_response import RunResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RunResponse from a JSON string
run_response_instance = RunResponse.from_json(json)
# print the JSON string representation of the object
print(RunResponse.to_json())

# convert the object into a dict
run_response_dict = run_response_instance.to_dict()
# create an instance of RunResponse from a dict
run_response_from_dict = RunResponse.from_dict(run_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


