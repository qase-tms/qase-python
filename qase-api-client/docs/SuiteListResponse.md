# SuiteListResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **bool** |  | [optional] 
**result** | [**SuiteListResponseAllOfResult**](SuiteListResponseAllOfResult.md) |  | [optional] 

## Example

```python
from qase.api_client_v1.models.suite_list_response import SuiteListResponse

# TODO update the JSON string below
json = "{}"
# create an instance of SuiteListResponse from a JSON string
suite_list_response_instance = SuiteListResponse.from_json(json)
# print the JSON string representation of the object
print(SuiteListResponse.to_json())

# convert the object into a dict
suite_list_response_dict = suite_list_response_instance.to_dict()
# create an instance of SuiteListResponse from a dict
suite_list_response_form_dict = suite_list_response.from_dict(suite_list_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


