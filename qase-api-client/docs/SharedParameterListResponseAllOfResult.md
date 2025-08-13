# SharedParameterListResponseAllOfResult


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**total** | **int** |  | 
**entities** | [**List[SharedParameter]**](SharedParameter.md) |  | 

## Example

```python
from qase.api_client_v1.models.shared_parameter_list_response_all_of_result import SharedParameterListResponseAllOfResult

# TODO update the JSON string below
json = "{}"
# create an instance of SharedParameterListResponseAllOfResult from a JSON string
shared_parameter_list_response_all_of_result_instance = SharedParameterListResponseAllOfResult.from_json(json)
# print the JSON string representation of the object
print(SharedParameterListResponseAllOfResult.to_json())

# convert the object into a dict
shared_parameter_list_response_all_of_result_dict = shared_parameter_list_response_all_of_result_instance.to_dict()
# create an instance of SharedParameterListResponseAllOfResult from a dict
shared_parameter_list_response_all_of_result_form_dict = shared_parameter_list_response_all_of_result.from_dict(shared_parameter_list_response_all_of_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


