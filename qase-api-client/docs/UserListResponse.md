# UserListResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **bool** |  | [optional] 
**result** | [**UserListResponseAllOfResult**](UserListResponseAllOfResult.md) |  | [optional] 

## Example

```python
from qase.api_client_v1.models.user_list_response import UserListResponse

# TODO update the JSON string below
json = "{}"
# create an instance of UserListResponse from a JSON string
user_list_response_instance = UserListResponse.from_json(json)
# print the JSON string representation of the object
print(UserListResponse.to_json())

# convert the object into a dict
user_list_response_dict = user_list_response_instance.to_dict()
# create an instance of UserListResponse from a dict
user_list_response_from_dict = UserListResponse.from_dict(user_list_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


