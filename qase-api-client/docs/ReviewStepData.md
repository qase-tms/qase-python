# ReviewStepData

A step of the proposed test case. When `steps_type` is `gherkin` the step carries the scenario in `value` and nothing else: a non-empty `action`, `expected_result`, `data`, `attachments`, `shared` or nested `steps` is rejected.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**action** | **str** | Step action text. Classic steps only. | [optional] 
**shared** | **str** | Hash of an existing shared step to insert at this position. | [optional] 
**expected_result** | **str** |  | [optional] 
**data** | **str** |  | [optional] 
**value** | **str** | Gherkin scenario text. Used when steps_type is \&quot;gherkin\&quot;. Example: \&quot;Given a user exists\\nWhen they log in\\nThen they see the dashboard\&quot; | [optional] 
**attachments** | **List[str]** | A list of Attachment hashes. | [optional] 
**steps** | **List[object]** | Nested steps may be passed here. Use same structure for them. | [optional] 

## Example

```python
from qase.api_client_v1.models.review_step_data import ReviewStepData

# TODO update the JSON string below
json = "{}"
# create an instance of ReviewStepData from a JSON string
review_step_data_instance = ReviewStepData.from_json(json)
# print the JSON string representation of the object
print(ReviewStepData.to_json())

# convert the object into a dict
review_step_data_dict = review_step_data_instance.to_dict()
# create an instance of ReviewStepData from a dict
review_step_data_from_dict = ReviewStepData.from_dict(review_step_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


