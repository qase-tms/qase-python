# ReviewUpdate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**reviewers** | **List[UUID]** | Author UUIDs of team members assigned as reviewers (see &#x60;GET /author&#x60;). When provided, replaces the current reviewer list; an empty array removes all reviewers. Omit to leave reviewers unchanged. | [optional] 
**proposed_case** | [**ReviewCaseData**](ReviewCaseData.md) | Sent fields are merged into the stored proposal. Changing the proposal resets all existing approvals; updating only the reviewers keeps them. | [optional] 

## Example

```python
from qase.api_client_v1.models.review_update import ReviewUpdate

# TODO update the JSON string below
json = "{}"
# create an instance of ReviewUpdate from a JSON string
review_update_instance = ReviewUpdate.from_json(json)
# print the JSON string representation of the object
print(ReviewUpdate.to_json())

# convert the object into a dict
review_update_dict = review_update_instance.to_dict()
# create an instance of ReviewUpdate from a dict
review_update_from_dict = ReviewUpdate.from_dict(review_update_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


