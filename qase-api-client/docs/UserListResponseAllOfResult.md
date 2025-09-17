# UserListResponseAllOfResult


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**total** | **int** |  | [optional] 
**filtered** | **int** |  | [optional] 
**count** | **int** |  | [optional] 
**entities** | [**List[User]**](User.md) |  | [optional] 

## Example

```python
from qase.api_client_v1.models.user_list_response_all_of_result import UserListResponseAllOfResult

# TODO update the JSON string below
json = "{}"
# create an instance of UserListResponseAllOfResult from a JSON string
user_list_response_all_of_result_instance = UserListResponseAllOfResult.from_json(json)
# print the JSON string representation of the object
print(UserListResponseAllOfResult.to_json())

# convert the object into a dict
user_list_response_all_of_result_dict = user_list_response_all_of_result_instance.to_dict()
# create an instance of UserListResponseAllOfResult from a dict
user_list_response_all_of_result_from_dict = UserListResponseAllOfResult.from_dict(user_list_response_all_of_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


