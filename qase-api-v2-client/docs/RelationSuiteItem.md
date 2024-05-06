# RelationSuiteItem


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**title** | **str** |  | 
**public_id** | **int** |  | [optional] 

## Example

```python
from src import RelationSuiteItem

# TODO update the JSON string below
json = "{}"
# create an instance of RelationSuiteItem from a JSON string
relation_suite_item_instance = RelationSuiteItem.from_json(json)
# print the JSON string representation of the object
print(RelationSuiteItem.to_json())

# convert the object into a dict
relation_suite_item_dict = relation_suite_item_instance.to_dict()
# create an instance of RelationSuiteItem from a dict
relation_suite_item_form_dict = relation_suite_item.from_dict(relation_suite_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


