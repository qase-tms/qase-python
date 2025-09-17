# ResultCreateBulk


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**results** | [**List[ResultCreate]**](ResultCreate.md) |  | 

## Example

```python
from qase.api_client_v1.models.result_create_bulk import ResultCreateBulk

# TODO update the JSON string below
json = "{}"
# create an instance of ResultCreateBulk from a JSON string
result_create_bulk_instance = ResultCreateBulk.from_json(json)
# print the JSON string representation of the object
print(ResultCreateBulk.to_json())

# convert the object into a dict
result_create_bulk_dict = result_create_bulk_instance.to_dict()
# create an instance of ResultCreateBulk from a dict
result_create_bulk_from_dict = ResultCreateBulk.from_dict(result_create_bulk_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


