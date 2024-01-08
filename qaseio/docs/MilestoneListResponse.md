# MilestoneListResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **bool** |  | [optional] 
**result** | [**MilestoneListResponseAllOfResult**](MilestoneListResponseAllOfResult.md) |  | [optional] 

## Example

```python
from qaseio.models.milestone_list_response import MilestoneListResponse

# TODO update the JSON string below
json = "{}"
# create an instance of MilestoneListResponse from a JSON string
milestone_list_response_instance = MilestoneListResponse.from_json(json)
# print the JSON string representation of the object
print MilestoneListResponse.to_json()

# convert the object into a dict
milestone_list_response_dict = milestone_list_response_instance.to_dict()
# create an instance of MilestoneListResponse from a dict
milestone_list_response_form_dict = milestone_list_response.from_dict(milestone_list_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


