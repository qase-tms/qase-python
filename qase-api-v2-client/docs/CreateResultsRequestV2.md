# CreateResultsRequestV2


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**results** | [**List[ResultCreate]**](ResultCreate.md) |  | [optional] 

## Example

```python
from qase.api_client_v2.models.create_results_request_v2 import CreateResultsRequestV2

# TODO update the JSON string below
json = "{}"
# create an instance of CreateResultsRequestV2 from a JSON string
create_results_request_v2_instance = CreateResultsRequestV2.from_json(json)
# print the JSON string representation of the object
print(CreateResultsRequestV2.to_json())

# convert the object into a dict
create_results_request_v2_dict = create_results_request_v2_instance.to_dict()
# create an instance of CreateResultsRequestV2 from a dict
create_results_request_v2_from_dict = CreateResultsRequestV2.from_dict(create_results_request_v2_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


