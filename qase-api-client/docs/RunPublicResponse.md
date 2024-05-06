# RunPublicResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **bool** |  | [optional] 
**result** | [**RunPublicResponseAllOfResult**](RunPublicResponseAllOfResult.md) |  | [optional] 

## Example

```python
from qase.api_client_v1.models.run_public_response import RunPublicResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RunPublicResponse from a JSON string
run_public_response_instance = RunPublicResponse.from_json(json)
# print the JSON string representation of the object
print(RunPublicResponse.to_json())

# convert the object into a dict
run_public_response_dict = run_public_response_instance.to_dict()
# create an instance of RunPublicResponse from a dict
run_public_response_form_dict = run_public_response.from_dict(run_public_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


