# ReviewProposedStep


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**action** | **str** | Step action text. Used for classic steps. For gherkin steps, use the \&quot;value\&quot; property instead. | [optional] 
**expected_result** | **str** |  | [optional] 
**data** | **str** |  | [optional] 
**value** | **str** | Gherkin scenario text. Used when steps_type is \&quot;gherkin\&quot;. | [optional] 
**shared** | **str** | Hash of the referenced shared step. | [optional] 
**attachments** | **List[str]** | A list of Attachment hashes. | [optional] 
**steps** | **List[object]** | Nested steps use the same structure. | [optional] 

## Example

```python
from qase.api_client_v1.models.review_proposed_step import ReviewProposedStep

# TODO update the JSON string below
json = "{}"
# create an instance of ReviewProposedStep from a JSON string
review_proposed_step_instance = ReviewProposedStep.from_json(json)
# print the JSON string representation of the object
print(ReviewProposedStep.to_json())

# convert the object into a dict
review_proposed_step_dict = review_proposed_step_instance.to_dict()
# create an instance of ReviewProposedStep from a dict
review_proposed_step_from_dict = ReviewProposedStep.from_dict(review_proposed_step_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


