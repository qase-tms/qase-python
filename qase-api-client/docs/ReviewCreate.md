# ReviewCreate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**case_id** | **int** | ID of the reviewed test case. When present an &#x60;edit&#x60; review is created, otherwise a &#x60;create&#x60; review with a new-case draft. | [optional] 
**reviewers** | **List[UUID]** | Author UUIDs of team members to assign as reviewers (see &#x60;GET /author&#x60;). | [optional] 
**proposed_case** | [**ReviewCaseData**](ReviewCaseData.md) | For &#x60;create&#x60; reviews &#x60;title&#x60; and all required project fields are required. For &#x60;edit&#x60; reviews send only the fields the proposal changes. | 

## Example

```python
from qase.api_client_v1.models.review_create import ReviewCreate

# TODO update the JSON string below
json = "{}"
# create an instance of ReviewCreate from a JSON string
review_create_instance = ReviewCreate.from_json(json)
# print the JSON string representation of the object
print(ReviewCreate.to_json())

# convert the object into a dict
review_create_dict = review_create_instance.to_dict()
# create an instance of ReviewCreate from a dict
review_create_from_dict = ReviewCreate.from_dict(review_create_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


