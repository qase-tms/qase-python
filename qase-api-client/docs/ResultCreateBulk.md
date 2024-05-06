# ResultcreateBulk


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**results** | [**List[ResultCreate]**](ResultCreate.md) |  | 

## Example

```python
from qase.api_client_v1.models.resultcreate_bulk import ResultcreateBulk

# TODO update the JSON string below
json = "{}"
# create an instance of ResultcreateBulk from a JSON string
resultcreate_bulk_instance = ResultcreateBulk.from_json(json)
# print the JSON string representation of the object
print(ResultcreateBulk.to_json())

# convert the object into a dict
resultcreate_bulk_dict = resultcreate_bulk_instance.to_dict()
# create an instance of ResultcreateBulk from a dict
resultcreate_bulk_form_dict = resultcreate_bulk.from_dict(resultcreate_bulk_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


