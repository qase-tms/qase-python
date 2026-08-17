# ReviewListResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **bool** |  | [optional] 
**result** | [**ReviewListResponseAllOfResult**](ReviewListResponseAllOfResult.md) |  | [optional] 

## Example

```python
from qase.api_client_v1.models.review_list_response import ReviewListResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ReviewListResponse from a JSON string
review_list_response_instance = ReviewListResponse.from_json(json)
# print the JSON string representation of the object
print(ReviewListResponse.to_json())

# convert the object into a dict
review_list_response_dict = review_list_response_instance.to_dict()
# create an instance of ReviewListResponse from a dict
review_list_response_from_dict = ReviewListResponse.from_dict(review_list_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


