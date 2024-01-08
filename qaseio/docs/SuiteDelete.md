# SuiteDelete


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**destination_id** | **int** | If provided, child test cases would be moved to suite with such ID. | [optional] 

## Example

```python
from qaseio.models.suite_delete import SuiteDelete

# TODO update the JSON string below
json = "{}"
# create an instance of SuiteDelete from a JSON string
suite_delete_instance = SuiteDelete.from_json(json)
# print the JSON string representation of the object
print SuiteDelete.to_json()

# convert the object into a dict
suite_delete_dict = suite_delete_instance.to_dict()
# create an instance of SuiteDelete from a dict
suite_delete_form_dict = suite_delete.from_dict(suite_delete_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


