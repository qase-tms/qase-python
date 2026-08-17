# ReviewBulkResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **bool** |  | [optional] 
**result** | [**ReviewBulkResponseAllOfResult**](ReviewBulkResponseAllOfResult.md) |  | [optional] 

## Example

```python
from qase.api_client_v1.models.review_bulk_response import ReviewBulkResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ReviewBulkResponse from a JSON string
review_bulk_response_instance = ReviewBulkResponse.from_json(json)
# print the JSON string representation of the object
print(ReviewBulkResponse.to_json())

# convert the object into a dict
review_bulk_response_dict = review_bulk_response_instance.to_dict()
# create an instance of ReviewBulkResponse from a dict
review_bulk_response_from_dict = ReviewBulkResponse.from_dict(review_bulk_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


