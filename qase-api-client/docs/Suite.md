# Suite


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | [optional] 
**title** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**preconditions** | **str** |  | [optional] 
**position** | **int** |  | [optional] 
**cases_count** | **int** |  | [optional] 
**parent_id** | **int** |  | [optional] 
**created** | **str** | Deprecated, use the &#x60;created_at&#x60; property instead. | [optional] 
**updated** | **str** | Deprecated, use the &#x60;updated_at&#x60; property instead. | [optional] 
**created_at** | **datetime** |  | [optional] 
**updated_at** | **datetime** |  | [optional] 

## Example

```python
from src.qase.api_client_v1.models.suite import Suite

# TODO update the JSON string below
json = "{}"
# create an instance of Suite from a JSON string
suite_instance = Suite.from_json(json)
# print the JSON string representation of the object
print(Suite.to_json())

# convert the object into a dict
suite_dict = suite_instance.to_dict()
# create an instance of Suite from a dict
suite_form_dict = suite.from_dict(suite_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


