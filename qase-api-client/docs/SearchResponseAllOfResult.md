# SearchResponseAllOfResult


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**entities** | [**List[SearchResponseAllOfResultEntities]**](SearchResponseAllOfResultEntities.md) |  | 
**total** | **int** |  | 

## Example

```python
from qase.api_client_v1.models.search_response_all_of_result import SearchResponseAllOfResult

# TODO update the JSON string below
json = "{}"
# create an instance of SearchResponseAllOfResult from a JSON string
search_response_all_of_result_instance = SearchResponseAllOfResult.from_json(json)
# print the JSON string representation of the object
print(SearchResponseAllOfResult.to_json())

# convert the object into a dict
search_response_all_of_result_dict = search_response_all_of_result_instance.to_dict()
# create an instance of SearchResponseAllOfResult from a dict
search_response_all_of_result_from_dict = SearchResponseAllOfResult.from_dict(search_response_all_of_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


