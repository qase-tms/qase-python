# SuiteResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **bool** |  | [optional] 
**result** | [**Suite**](Suite.md) |  | [optional] 

## Example

```python
from qaseio.models.suite_response import SuiteResponse

# TODO update the JSON string below
json = "{}"
# create an instance of SuiteResponse from a JSON string
suite_response_instance = SuiteResponse.from_json(json)
# print the JSON string representation of the object
print SuiteResponse.to_json()

# convert the object into a dict
suite_response_dict = suite_response_instance.to_dict()
# create an instance of SuiteResponse from a dict
suite_response_form_dict = suite_response.from_dict(suite_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


