# AuthorListResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **bool** |  | [optional] 
**result** | [**AuthorListResponseAllOfResult**](AuthorListResponseAllOfResult.md) |  | [optional] 

## Example

```python
from qase.api_client_v1.models.author_list_response import AuthorListResponse

# TODO update the JSON string below
json = "{}"
# create an instance of AuthorListResponse from a JSON string
author_list_response_instance = AuthorListResponse.from_json(json)
# print the JSON string representation of the object
print(AuthorListResponse.to_json())

# convert the object into a dict
author_list_response_dict = author_list_response_instance.to_dict()
# create an instance of AuthorListResponse from a dict
author_list_response_from_dict = AuthorListResponse.from_dict(author_list_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


