# ReviewProposedCase

The test case state proposed by the review. Only the fields the proposal carries are present.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**title** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**preconditions** | **str** |  | [optional] 
**postconditions** | **str** |  | [optional] 
**severity** | **int** |  | [optional] 
**priority** | **int** |  | [optional] 
**behavior** | **int** |  | [optional] 
**type** | **int** |  | [optional] 
**layer** | **int** |  | [optional] 
**is_flaky** | **int** |  | [optional] 
**is_muted** | **bool** |  | [optional] 
**suite_id** | **int** |  | [optional] 
**milestone_id** | **int** |  | [optional] 
**is_manual** | **bool** | &#x60;true&#x60; if the case is manual, &#x60;false&#x60; if it is automated. | [optional] 
**is_to_be_automated** | **bool** | &#x60;true&#x60; if a manual case is planned to be automated. | [optional] 
**status** | **int** |  | [optional] 
**steps_type** | **str** |  | [optional] 
**attachments** | **List[str]** | Attachment hashes. | [optional] 
**steps** | [**List[ReviewProposedStep]**](ReviewProposedStep.md) |  | [optional] 
**tags** | **List[str]** |  | [optional] 
**parameters** | [**List[TestCaseParameter]**](TestCaseParameter.md) |  | [optional] 
**custom_fields** | [**List[CustomFieldValue]**](CustomFieldValue.md) |  | [optional] 

## Example

```python
from qase.api_client_v1.models.review_proposed_case import ReviewProposedCase

# TODO update the JSON string below
json = "{}"
# create an instance of ReviewProposedCase from a JSON string
review_proposed_case_instance = ReviewProposedCase.from_json(json)
# print the JSON string representation of the object
print(ReviewProposedCase.to_json())

# convert the object into a dict
review_proposed_case_dict = review_proposed_case_instance.to_dict()
# create an instance of ReviewProposedCase from a dict
review_proposed_case_from_dict = ReviewProposedCase.from_dict(review_proposed_case_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


