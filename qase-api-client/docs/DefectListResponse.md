# DefectListResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **bool** |  | [optional] 
**result** | [**DefectListResponseAllOfResult**](DefectListResponseAllOfResult.md) |  | [optional] 

## Example

```python
from qase.api_client_v1.models.defect_list_response import DefectListResponse

# TODO update the JSON string below
json = "{}"
# create an instance of DefectListResponse from a JSON string
defect_list_response_instance = DefectListResponse.from_json(json)
# print the JSON string representation of the object
print(DefectListResponse.to_json())

# convert the object into a dict
defect_list_response_dict = defect_list_response_instance.to_dict()
# create an instance of DefectListResponse from a dict
defect_list_response_form_dict = defect_list_response.from_dict(defect_list_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


