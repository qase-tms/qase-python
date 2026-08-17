# ReviewCaseData

The test case fields proposed by the review.

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
**is_muted** | **bool** | Mute state of the proposed test case. | [optional] 
**suite_id** | **int** |  | [optional] 
**milestone_id** | **int** |  | [optional] 
**is_manual** | **bool** | &#x60;true&#x60; if the case is manual, &#x60;false&#x60; if it is automated. | [optional] 
**is_to_be_automated** | **bool** | &#x60;true&#x60; if a manual case is planned to be automated. | [optional] 
**status** | **int** |  | [optional] 
**steps_type** | **str** | Format of the steps field. Omit to keep the current one, &#x60;classic&#x60; for a new-case draft; changing it requires sending &#x60;steps&#x60; in the same request. | [optional] 
**attachments** | **List[str]** | A list of Attachment hashes. | [optional] 
**steps** | [**List[ReviewStepData]**](ReviewStepData.md) | For gherkin steps send the scenario in &#x60;value&#x60;. | [optional] 
**tags** | **List[str]** |  | [optional] 
**parameters** | [**List[TestCaseParameterCreate]**](TestCaseParameterCreate.md) |  | [optional] 
**custom_field** | **Dict[str, str]** | Map of custom field ID to value. A &#x60;create&#x60; review must carry every required custom field. An &#x60;edit&#x60; review is validated against the current test case, so send only the fields the proposal changes. | [optional] 

## Example

```python
from qase.api_client_v1.models.review_case_data import ReviewCaseData

# TODO update the JSON string below
json = "{}"
# create an instance of ReviewCaseData from a JSON string
review_case_data_instance = ReviewCaseData.from_json(json)
# print the JSON string representation of the object
print(ReviewCaseData.to_json())

# convert the object into a dict
review_case_data_dict = review_case_data_instance.to_dict()
# create an instance of ReviewCaseData from a dict
review_case_data_from_dict = ReviewCaseData.from_dict(review_case_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


