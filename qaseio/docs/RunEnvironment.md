# RunEnvironment


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**title** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**slug** | **str** |  | [optional] 
**host** | **str** |  | [optional] 

## Example

```python
from qaseio.models.run_environment import RunEnvironment

# TODO update the JSON string below
json = "{}"
# create an instance of RunEnvironment from a JSON string
run_environment_instance = RunEnvironment.from_json(json)
# print the JSON string representation of the object
print RunEnvironment.to_json()

# convert the object into a dict
run_environment_dict = run_environment_instance.to_dict()
# create an instance of RunEnvironment from a dict
run_environment_form_dict = run_environment.from_dict(run_environment_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


