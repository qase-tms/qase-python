# PlanListResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **bool** |  | [optional] 
**result** | [**PlanListResponseAllOfResult**](PlanListResponseAllOfResult.md) |  | [optional] 

## Example

```python
from qase.api_client_v1.models.plan_list_response import PlanListResponse

# TODO update the JSON string below
json = "{}"
# create an instance of PlanListResponse from a JSON string
plan_list_response_instance = PlanListResponse.from_json(json)
# print the JSON string representation of the object
print(PlanListResponse.to_json())

# convert the object into a dict
plan_list_response_dict = plan_list_response_instance.to_dict()
# create an instance of PlanListResponse from a dict
plan_list_response_from_dict = PlanListResponse.from_dict(plan_list_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


