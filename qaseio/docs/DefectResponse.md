# DefectResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **bool** |  | [optional] 
**result** | [**Defect**](Defect.md) |  | [optional] 

## Example

```python
from qaseio.models.defect_response import DefectResponse

# TODO update the JSON string below
json = "{}"
# create an instance of DefectResponse from a JSON string
defect_response_instance = DefectResponse.from_json(json)
# print the JSON string representation of the object
print DefectResponse.to_json()

# convert the object into a dict
defect_response_dict = defect_response_instance.to_dict()
# create an instance of DefectResponse from a dict
defect_response_form_dict = defect_response.from_dict(defect_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


