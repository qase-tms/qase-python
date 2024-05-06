# BaseErrorResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**error_message** | **str** |  | [optional] 

## Example

```python
from src import BaseErrorResponse

# TODO update the JSON string below
json = "{}"
# create an instance of BaseErrorResponse from a JSON string
base_error_response_instance = BaseErrorResponse.from_json(json)
# print the JSON string representation of the object
print(BaseErrorResponse.to_json())

# convert the object into a dict
base_error_response_dict = base_error_response_instance.to_dict()
# create an instance of BaseErrorResponse from a dict
base_error_response_form_dict = base_error_response.from_dict(base_error_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


