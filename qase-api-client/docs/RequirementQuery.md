# RequirementQuery


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | [optional] 
**requirement_id** | **int** |  | 
**parent_id** | **int** |  | [optional] 
**member_id** | **int** |  | [optional] 
**title** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**status** | **str** |  | [optional] 
**type** | **str** |  | [optional] 
**created_at** | **datetime** |  | [optional] 
**updated_at** | **datetime** |  | [optional] 

## Example

```python
from qase.api_client_v1.models.requirement_query import RequirementQuery

# TODO update the JSON string below
json = "{}"
# create an instance of RequirementQuery from a JSON string
requirement_query_instance = RequirementQuery.from_json(json)
# print the JSON string representation of the object
print(RequirementQuery.to_json())

# convert the object into a dict
requirement_query_dict = requirement_query_instance.to_dict()
# create an instance of RequirementQuery from a dict
requirement_query_from_dict = RequirementQuery.from_dict(requirement_query_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


