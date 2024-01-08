# MilestoneResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **bool** |  | [optional] 
**result** | [**Milestone**](Milestone.md) |  | [optional] 

## Example

```python
from qaseio.models.milestone_response import MilestoneResponse

# TODO update the JSON string below
json = "{}"
# create an instance of MilestoneResponse from a JSON string
milestone_response_instance = MilestoneResponse.from_json(json)
# print the JSON string representation of the object
print MilestoneResponse.to_json()

# convert the object into a dict
milestone_response_dict = milestone_response_instance.to_dict()
# create an instance of MilestoneResponse from a dict
milestone_response_form_dict = milestone_response.from_dict(milestone_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


