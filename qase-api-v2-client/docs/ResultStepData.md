# ResultStepData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**action** | **str** |  | 
**expected_result** | **str** |  | [optional] 
**input_data** | **str** |  | [optional] 
**attachments** | **List[str]** |  | [optional] 

## Example

```python
from src.qase.models import ResultStepData

# TODO update the JSON string below
json = "{}"
# create an instance of ResultStepData from a JSON string
result_step_data_instance = ResultStepData.from_json(json)
# print the JSON string representation of the object
print(ResultStepData.to_json())

# convert the object into a dict
result_step_data_dict = result_step_data_instance.to_dict()
# create an instance of ResultStepData from a dict
result_step_data_form_dict = result_step_data.from_dict(result_step_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


