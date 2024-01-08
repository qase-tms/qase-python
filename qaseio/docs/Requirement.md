# Requirement


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | [optional] 
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
from qaseio.models.requirement import Requirement

# TODO update the JSON string below
json = "{}"
# create an instance of Requirement from a JSON string
requirement_instance = Requirement.from_json(json)
# print the JSON string representation of the object
print Requirement.to_json()

# convert the object into a dict
requirement_dict = requirement_instance.to_dict()
# create an instance of Requirement from a dict
requirement_form_dict = requirement.from_dict(requirement_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


