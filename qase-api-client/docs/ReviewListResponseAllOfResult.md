# ReviewListResponseAllOfResult


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**total** | **int** |  | [optional] 
**filtered** | **int** |  | [optional] 
**count** | **int** |  | [optional] 
**entities** | [**List[Review]**](Review.md) |  | [optional] 

## Example

```python
from qase.api_client_v1.models.review_list_response_all_of_result import ReviewListResponseAllOfResult

# TODO update the JSON string below
json = "{}"
# create an instance of ReviewListResponseAllOfResult from a JSON string
review_list_response_all_of_result_instance = ReviewListResponseAllOfResult.from_json(json)
# print the JSON string representation of the object
print(ReviewListResponseAllOfResult.to_json())

# convert the object into a dict
review_list_response_all_of_result_dict = review_list_response_all_of_result_instance.to_dict()
# create an instance of ReviewListResponseAllOfResult from a dict
review_list_response_all_of_result_from_dict = ReviewListResponseAllOfResult.from_dict(review_list_response_all_of_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


