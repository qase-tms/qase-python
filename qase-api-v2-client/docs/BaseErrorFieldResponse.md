# BaseErrorFieldResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**error_fields** | [**List[BaseErrorFieldResponseErrorFieldsInner]**](BaseErrorFieldResponseErrorFieldsInner.md) |  | [optional] 

## Example

```python
from qase.api_clinet_v2.models import BaseErrorFieldResponse

# TODO update the JSON string below
json = "{}"
# create an instance of BaseErrorFieldResponse from a JSON string
base_error_field_response_instance = BaseErrorFieldResponse.from_json(json)
# print the JSON string representation of the object
print(BaseErrorFieldResponse.to_json())

# convert the object into a dict
base_error_field_response_dict = base_error_field_response_instance.to_dict()
# create an instance of BaseErrorFieldResponse from a dict
base_error_field_response_form_dict = base_error_field_response.from_dict(base_error_field_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


