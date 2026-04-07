# RelationSuite


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**List[RelationSuiteItem]**](RelationSuiteItem.md) |  | 

## Example

```python
from qase.api_client_v2.models.relation_suite import RelationSuite

# TODO update the JSON string below
json = "{}"
# create an instance of RelationSuite from a JSON string
relation_suite_instance = RelationSuite.from_json(json)
# print the JSON string representation of the object
print(RelationSuite.to_json())

# convert the object into a dict
relation_suite_dict = relation_suite_instance.to_dict()
# create an instance of RelationSuite from a dict
relation_suite_from_dict = RelationSuite.from_dict(relation_suite_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


