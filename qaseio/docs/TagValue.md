# TagValue


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**title** | **str** |  | [optional] 
**internal_id** | **int** |  | [optional] 

## Example

```python
from qaseio.models.tag_value import TagValue

# TODO update the JSON string below
json = "{}"
# create an instance of TagValue from a JSON string
tag_value_instance = TagValue.from_json(json)
# print the JSON string representation of the object
print TagValue.to_json()

# convert the object into a dict
tag_value_dict = tag_value_instance.to_dict()
# create an instance of TagValue from a dict
tag_value_form_dict = tag_value.from_dict(tag_value_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


