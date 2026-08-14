# ReviewBulkResponseAllOfResult


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**items** | [**List[ReviewBulkResponseAllOfResultItems]**](ReviewBulkResponseAllOfResultItems.md) | Per-item outcomes, in request order. | [optional] 

## Example

```python
from qase.api_client_v1.models.review_bulk_response_all_of_result import ReviewBulkResponseAllOfResult

# TODO update the JSON string below
json = "{}"
# create an instance of ReviewBulkResponseAllOfResult from a JSON string
review_bulk_response_all_of_result_instance = ReviewBulkResponseAllOfResult.from_json(json)
# print the JSON string representation of the object
print(ReviewBulkResponseAllOfResult.to_json())

# convert the object into a dict
review_bulk_response_all_of_result_dict = review_bulk_response_all_of_result_instance.to_dict()
# create an instance of ReviewBulkResponseAllOfResult from a dict
review_bulk_response_all_of_result_from_dict = ReviewBulkResponseAllOfResult.from_dict(review_bulk_response_all_of_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


