# SearchResponseAllOfResultEntities


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | [optional] 
**title** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**status** | **str** |  | [optional] 
**status_text** | **str** |  | [optional] 
**start_time** | **datetime** |  | [optional] 
**end_time** | **datetime** |  | [optional] 
**public** | **bool** |  | [optional] 
**stats** | [**RunStats**](RunStats.md) |  | [optional] 
**time_spent** | **int** | Time in ms. | [optional] 
**environment** | [**RunEnvironment**](RunEnvironment.md) |  | [optional] 
**milestone** | [**RunMilestone**](RunMilestone.md) |  | [optional] 
**custom_fields** | [**List[CustomFieldValue]**](CustomFieldValue.md) |  | [optional] 
**tags** | [**List[TagValue]**](TagValue.md) |  | [optional] 
**cases** | **List[int]** |  | [optional] 
**hash** | **str** |  | [optional] 
**comment** | **str** |  | [optional] 
**stacktrace** | **str** |  | [optional] 
**run_id** | **int** |  | [optional] 
**case_id** | **int** |  | [optional] 
**steps** | [**List[TestStep]**](TestStep.md) |  | [optional] 
**is_api_result** | **bool** |  | [optional] 
**time_spent_ms** | **int** |  | [optional] 
**attachments** | [**List[Attachment]**](Attachment.md) |  | [optional] 
**parent_id** | **int** |  | [optional] 
**member_id** | **int** | Deprecated, use &#x60;author_id&#x60; instead. | [optional] 
**type** | **int** |  | [optional] 
**created_at** | **datetime** |  | [optional] 
**updated_at** | **datetime** |  | [optional] 
**position** | **int** |  | [optional] 
**preconditions** | **str** |  | [optional] 
**postconditions** | **str** |  | [optional] 
**severity** | **str** |  | [optional] 
**priority** | **int** |  | [optional] 
**layer** | **int** |  | [optional] 
**is_flaky** | **int** |  | [optional] 
**behavior** | **int** |  | [optional] 
**automation** | **int** |  | [optional] 
**milestone_id** | **int** |  | [optional] 
**suite_id** | **int** |  | [optional] 
**steps_type** | **str** |  | [optional] 
**params** | [**TestCaseParams**](TestCaseParams.md) |  | [optional] 
**author_id** | **int** |  | [optional] 
**actual_result** | **str** |  | [optional] 
**resolved** | **datetime** |  | [optional] 
**external_data** | **str** |  | [optional] 
**cases_count** | **int** |  | [optional] 

## Example

```python
from qase.api_client_v1.models.search_response_all_of_result_entities import SearchResponseAllOfResultEntities

# TODO update the JSON string below
json = "{}"
# create an instance of SearchResponseAllOfResultEntities from a JSON string
search_response_all_of_result_entities_instance = SearchResponseAllOfResultEntities.from_json(json)
# print the JSON string representation of the object
print(SearchResponseAllOfResultEntities.to_json())

# convert the object into a dict
search_response_all_of_result_entities_dict = search_response_all_of_result_entities_instance.to_dict()
# create an instance of SearchResponseAllOfResultEntities from a dict
search_response_all_of_result_entities_form_dict = search_response_all_of_result_entities.from_dict(
    search_response_all_of_result_entities_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


