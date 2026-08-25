# ResultExecution


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**start_time** | **float** | Unix epoch time in seconds (whole part) and milliseconds (fractional part). | [optional] 
**end_time** | **float** | Unix epoch time in seconds (whole part) and milliseconds (fractional part). | [optional] 
**status** | **str** | Can have the following values passed, failed, blocked, skipped, invalid + custom statuses | 
**duration** | **int** | Duration of the test execution in milliseconds. | [optional] 
**stacktrace** | **str** |  | [optional] 
**error_context** | **str** | Free-form failure context captured by the reporter. For Playwright this is the content of error-context.md (test info, error details, page snapshot), so it may include rendered page content. Stored verbatim so it can be copied as raw text. Values longer than 262144 characters are silently truncated by Qase and the request still succeeds. Write-only — not returned by the result read endpoints. | [optional] 
**thread** | **str** |  | [optional] 

## Example

```python
from qase.api_client_v2.models.result_execution import ResultExecution

# TODO update the JSON string below
json = "{}"
# create an instance of ResultExecution from a JSON string
result_execution_instance = ResultExecution.from_json(json)
# print the JSON string representation of the object
print(ResultExecution.to_json())

# convert the object into a dict
result_execution_dict = result_execution_instance.to_dict()
# create an instance of ResultExecution from a dict
result_execution_from_dict = ResultExecution.from_dict(result_execution_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


