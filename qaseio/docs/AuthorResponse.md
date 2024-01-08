# AuthorResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **bool** |  | [optional] 
**result** | [**Author**](Author.md) |  | [optional] 

## Example

```python
from qaseio.models.author_response import AuthorResponse

# TODO update the JSON string below
json = "{}"
# create an instance of AuthorResponse from a JSON string
author_response_instance = AuthorResponse.from_json(json)
# print the JSON string representation of the object
print AuthorResponse.to_json()

# convert the object into a dict
author_response_dict = author_response_instance.to_dict()
# create an instance of AuthorResponse from a dict
author_response_form_dict = author_response.from_dict(author_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


