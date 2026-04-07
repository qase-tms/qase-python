# ResultCreateBulkResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **bool** |  | [optional] 

## Example

```python
from qase.api_client_v2.models.result_create_bulk_response import ResultCreateBulkResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ResultCreateBulkResponse from a JSON string
result_create_bulk_response_instance = ResultCreateBulkResponse.from_json(json)
# print the JSON string representation of the object
print(ResultCreateBulkResponse.to_json())

# convert the object into a dict
result_create_bulk_response_dict = result_create_bulk_response_instance.to_dict()
# create an instance of ResultCreateBulkResponse from a dict
result_create_bulk_response_from_dict = ResultCreateBulkResponse.from_dict(result_create_bulk_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


