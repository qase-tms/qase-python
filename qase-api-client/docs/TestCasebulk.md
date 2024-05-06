# TestCasebulk


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**cases** | [**List[TestCasebulkCasesInner]**](TestCasebulkCasesInner.md) |  | 

## Example

```python
from qase.api_client_v1.models.test_casebulk import TestCasebulk

# TODO update the JSON string below
json = "{}"
# create an instance of TestCasebulk from a JSON string
test_casebulk_instance = TestCasebulk.from_json(json)
# print the JSON string representation of the object
print(TestCasebulk.to_json())

# convert the object into a dict
test_casebulk_dict = test_casebulk_instance.to_dict()
# create an instance of TestCasebulk from a dict
test_casebulk_form_dict = test_casebulk.from_dict(test_casebulk_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


