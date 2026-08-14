# ReviewBulk


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**reviews** | [**List[ReviewCreate]**](ReviewCreate.md) | Validated as a whole: if any item is invalid nothing is created. Otherwise each item is processed on its own and reported in the response. | 

## Example

```python
from qase.api_client_v1.models.review_bulk import ReviewBulk

# TODO update the JSON string below
json = "{}"
# create an instance of ReviewBulk from a JSON string
review_bulk_instance = ReviewBulk.from_json(json)
# print the JSON string representation of the object
print(ReviewBulk.to_json())

# convert the object into a dict
review_bulk_dict = review_bulk_instance.to_dict()
# create an instance of ReviewBulk from a dict
review_bulk_from_dict = ReviewBulk.from_dict(review_bulk_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


