# PlanResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **bool** |  | [optional] 
**result** | [**PlanDetailed**](PlanDetailed.md) |  | [optional] 

## Example

```python
from qase.api_client_v1.models.plan_response import PlanResponse

# TODO update the JSON string below
json = "{}"
# create an instance of PlanResponse from a JSON string
plan_response_instance = PlanResponse.from_json(json)
# print the JSON string representation of the object
print(PlanResponse.to_json())

# convert the object into a dict
plan_response_dict = plan_response_instance.to_dict()
# create an instance of PlanResponse from a dict
plan_response_form_dict = plan_response.from_dict(plan_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


