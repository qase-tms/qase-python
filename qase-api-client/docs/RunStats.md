# RunStats


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**total** | **int** |  | [optional] 
**statuses** | **Dict[str, int]** |  | [optional] 
**untested** | **int** |  | [optional] 
**passed** | **int** |  | [optional] 
**failed** | **int** |  | [optional] 
**blocked** | **int** |  | [optional] 
**skipped** | **int** |  | [optional] 
**retest** | **int** |  | [optional] 
**in_progress** | **int** |  | [optional] 
**invalid** | **int** |  | [optional] 

## Example

```python
from qase.api_client_v1.models.run_stats import RunStats

# TODO update the JSON string below
json = "{}"
# create an instance of RunStats from a JSON string
run_stats_instance = RunStats.from_json(json)
# print the JSON string representation of the object
print(RunStats.to_json())

# convert the object into a dict
run_stats_dict = run_stats_instance.to_dict()
# create an instance of RunStats from a dict
run_stats_from_dict = RunStats.from_dict(run_stats_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


