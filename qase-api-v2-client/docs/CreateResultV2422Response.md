# CreateResultV2422Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**error_message** | **str** |  | [optional] 
**error_fields** | [**List[BaseErrorFieldResponseErrorFieldsInner]**](BaseErrorFieldResponseErrorFieldsInner.md) |  | [optional] 

## Example

```python
from qase.api_client_v2.models.create_result_v2422_response import CreateResultV2422Response

# TODO update the JSON string below
json = "{}"
# create an instance of CreateResultV2422Response from a JSON string
create_result_v2422_response_instance = CreateResultV2422Response.from_json(json)
# print the JSON string representation of the object
print(CreateResultV2422Response.to_json())

# convert the object into a dict
create_result_v2422_response_dict = create_result_v2422_response_instance.to_dict()
# create an instance of CreateResultV2422Response from a dict
create_result_v2422_response_form_dict = create_result_v2422_response.from_dict(create_result_v2422_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


