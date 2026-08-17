# Review


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** | Review ID, unique within the project. | [optional] 
**title** | **str** |  | [optional] 
**type** | **str** | &#x60;create&#x60; — the review proposes a new test case; &#x60;edit&#x60; — the review proposes changes to an existing test case. | [optional] 
**status** | **str** |  | [optional] 
**case_id** | **int** | ID of the reviewed test case. Null for new-case draft reviews. | [optional] 
**author_uuid** | **UUID** | Author UUID of the review creator (see &#x60;GET /author&#x60;). | [optional] 
**reviewers** | [**List[ReviewReviewersInner]**](ReviewReviewersInner.md) |  | [optional] 
**created_at** | **datetime** |  | [optional] 
**updated_at** | **datetime** |  | [optional] 

## Example

```python
from qase.api_client_v1.models.review import Review

# TODO update the JSON string below
json = "{}"
# create an instance of Review from a JSON string
review_instance = Review.from_json(json)
# print the JSON string representation of the object
print(Review.to_json())

# convert the object into a dict
review_dict = review_instance.to_dict()
# create an instance of Review from a dict
review_from_dict = Review.from_dict(review_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


