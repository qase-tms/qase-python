# ReviewBulkResponseAllOfResultItems


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**review_id** | **int** | ID of the created review. Null when the item failed. | [optional] 
**case_id** | **int** | The &#x60;case_id&#x60; submitted with the item, echoed back for correlation. Null for new-case draft reviews. | [optional] 
**error** | **str** | Failure reason. Null when the item was created. | [optional] 

## Example

```python
from qase.api_client_v1.models.review_bulk_response_all_of_result_items import ReviewBulkResponseAllOfResultItems

# TODO update the JSON string below
json = "{}"
# create an instance of ReviewBulkResponseAllOfResultItems from a JSON string
review_bulk_response_all_of_result_items_instance = ReviewBulkResponseAllOfResultItems.from_json(json)
# print the JSON string representation of the object
print(ReviewBulkResponseAllOfResultItems.to_json())

# convert the object into a dict
review_bulk_response_all_of_result_items_dict = review_bulk_response_all_of_result_items_instance.to_dict()
# create an instance of ReviewBulkResponseAllOfResultItems from a dict
review_bulk_response_all_of_result_items_from_dict = ReviewBulkResponseAllOfResultItems.from_dict(review_bulk_response_all_of_result_items_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


