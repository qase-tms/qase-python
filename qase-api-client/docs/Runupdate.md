# Runupdate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**title** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**environment_id** | **int** |  | [optional] 
**environment_slug** | **str** |  | [optional] 
**milestone_id** | **int** |  | [optional] 
**tags** | **List[str]** |  | [optional] 
**configurations** | **List[int]** |  | [optional] 
**custom_field** | **Dict[str, str]** | A map of custom fields values (id &#x3D;&gt; value) | [optional] 

## Example

```python
from qase.api_client_v1.models.runupdate import Runupdate

# TODO update the JSON string below
json = "{}"
# create an instance of Runupdate from a JSON string
runupdate_instance = Runupdate.from_json(json)
# print the JSON string representation of the object
print(Runupdate.to_json())

# convert the object into a dict
runupdate_dict = runupdate_instance.to_dict()
# create an instance of Runupdate from a dict
runupdate_form_dict = runupdate.from_dict(runupdate_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


