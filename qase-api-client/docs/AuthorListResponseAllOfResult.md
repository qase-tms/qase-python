# AuthorListResponseAllOfResult


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**total** | **int** |  | [optional] 
**filtered** | **int** |  | [optional] 
**count** | **int** |  | [optional] 
**entities** | [**List[Author]**](Author.md) |  | [optional] 

## Example

```python
from src.qase.api_client_v1.models.author_list_response_all_of_result import AuthorListResponseAllOfResult

# TODO update the JSON string below
json = "{}"
# create an instance of AuthorListResponseAllOfResult from a JSON string
author_list_response_all_of_result_instance = AuthorListResponseAllOfResult.from_json(json)
# print the JSON string representation of the object
print(AuthorListResponseAllOfResult.to_json())

# convert the object into a dict
author_list_response_all_of_result_dict = author_list_response_all_of_result_instance.to_dict()
# create an instance of AuthorListResponseAllOfResult from a dict
author_list_response_all_of_result_form_dict = author_list_response_all_of_result.from_dict(
    author_list_response_all_of_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


