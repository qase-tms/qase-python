# ReviewReviewersInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**author_uuid** | **UUID** | Author UUID of the reviewer (see &#x60;GET /author&#x60;). | [optional] 
**status** | **str** |  | [optional] 

## Example

```python
from qase.api_client_v1.models.review_reviewers_inner import ReviewReviewersInner

# TODO update the JSON string below
json = "{}"
# create an instance of ReviewReviewersInner from a JSON string
review_reviewers_inner_instance = ReviewReviewersInner.from_json(json)
# print the JSON string representation of the object
print(ReviewReviewersInner.to_json())

# convert the object into a dict
review_reviewers_inner_dict = review_reviewers_inner_instance.to_dict()
# create an instance of ReviewReviewersInner from a dict
review_reviewers_inner_from_dict = ReviewReviewersInner.from_dict(review_reviewers_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


