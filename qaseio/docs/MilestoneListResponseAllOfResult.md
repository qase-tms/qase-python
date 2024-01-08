# MilestoneListResponseAllOfResult


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**total** | **int** |  | [optional] 
**filtered** | **int** |  | [optional] 
**count** | **int** |  | [optional] 
**entities** | [**List[Milestone]**](Milestone.md) |  | [optional] 

## Example

```python
from qaseio.models.milestone_list_response_all_of_result import MilestoneListResponseAllOfResult

# TODO update the JSON string below
json = "{}"
# create an instance of MilestoneListResponseAllOfResult from a JSON string
milestone_list_response_all_of_result_instance = MilestoneListResponseAllOfResult.from_json(json)
# print the JSON string representation of the object
print MilestoneListResponseAllOfResult.to_json()

# convert the object into a dict
milestone_list_response_all_of_result_dict = milestone_list_response_all_of_result_instance.to_dict()
# create an instance of MilestoneListResponseAllOfResult from a dict
milestone_list_response_all_of_result_form_dict = milestone_list_response_all_of_result.from_dict(milestone_list_response_all_of_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


