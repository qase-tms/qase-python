# ResultRelations


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**suite** | [**RelationSuite**](RelationSuite.md) |  | [optional] 

## Example

```python
from qaseio.models.result_relations import ResultRelations

# TODO update the JSON string below
json = "{}"
# create an instance of ResultRelations from a JSON string
result_relations_instance = ResultRelations.from_json(json)
# print the JSON string representation of the object
print ResultRelations.to_json()

# convert the object into a dict
result_relations_dict = result_relations_instance.to_dict()
# create an instance of ResultRelations from a dict
result_relations_form_dict = result_relations.from_dict(result_relations_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


